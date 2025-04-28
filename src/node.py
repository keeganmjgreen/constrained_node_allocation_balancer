from __future__ import annotations

import dataclasses
from itertools import groupby

from treelib import Tree

from ascii_barplot import make_ascii_barplot


@dataclasses.dataclass
class Node:
    id: str = dataclasses.field(init=False)
    _id_suffix: str = dataclasses.field(init=False)
    limit: float | None = None
    children: list[Node] = dataclasses.field(default_factory=list)
    parent: Node | None = dataclasses.field(default=None, repr=False)
    level: int = dataclasses.field(init=False, repr=False)
    allotment: float = 0.0

    def __post_init__(self):
        for child in self.children:
            child.parent = self
        # Set IDs and levels if this is the root node:
        if self.parent is None:
            self._set_ids()
            self._set_levels()

    def _set_ids(
        self, starting_at: str = "1", parent_id: str | None = None, separator: str = "|"
    ) -> None:
        self._id_suffix = starting_at
        if self.parent is None:
            self.id = self._id_suffix
        else:
            self.id = parent_id + separator + self._id_suffix
        for i, child in enumerate(self.children):
            child._set_ids(starting_at=str(i + 1), parent_id=self.id)

    def _set_levels(self, starting_level: int = 0) -> None:
        self.level = starting_level
        for child in self.children:
            child._set_levels(starting_level=(self.level + 1))

    @property
    def remaining_budget(self) -> float | None:
        if self.limit is not None:
            return self.limit - self.allotment

    @property
    def limit_exceeded(self) -> bool:
        return self.limit is not None and self.allotment > self.limit

    @property
    def has_headroom(self) -> bool:
        return self.limit is None or self.allotment < self.limit

    @property
    def nodes_by_level(self) -> dict[int, list[Node]]:
        return {
            k: list(g)
            for k, g in groupby(
                sorted([self, *self.all_descendents], key=(lambda node: node.level)),
                key=(lambda node: node.level),
            )
        }

    @property
    def all_descendents(self) -> list[Node]:
        descendents: list[Node] = []
        for child in self.children:
            descendents.append(child)
            descendents += child.all_descendents
        return descendents

    @property
    def all_leaves(self) -> list[Node]:
        leaves: list[Node] = []
        for child in self.children:
            if len(child.children) > 0:
                leaves += child.all_leaves
            else:
                leaves.append(child)
        return leaves

    @property
    def n_leaves_at_or_below(self) -> int:
        """Return the number of leaves under the node, or `1` if the node is a leaf."""
        return len(self.all_leaves) or 1

    @property
    def all_leaf_allotments(self) -> dict[str, float]:
        return {leaf.id: leaf.allotment for leaf in self.all_leaves}

    @property
    def ancestor_chain(self) -> list[Node]:
        ancestor_chain: list[Node] = []
        if self.parent is not None:
            ancestor_chain.append(self.parent)
            if self.parent.parent is not None:
                ancestor_chain += self.parent.ancestor_chain
        return ancestor_chain

    @property
    def neighbors(self) -> list[Node] | None:
        if self.parent is not None:
            return [n for n in self.parent.nodes_by_level[self.level] if n is not self]

    @property
    def neighbors_with_headroom(self) -> list[Node] | None:
        if self.parent is not None:
            return [n for n in self.neighbors if n.has_headroom]

    def show(self) -> None:
        tree = Tree()
        all_nodes = [self, *self.all_descendents]
        max_id_suffix_len = max(len(n._id_suffix) for n in all_nodes)
        max_depth = max(n.level for n in all_nodes)
        max_allotment_str_len = max(len(f"{n.allotment:.3f}") for n in all_nodes)
        max_limit_str_len = max(
            len(f"{n.limit:.3f}") for n in all_nodes if n.limit is not None
        )
        max_limit = max(n.limit for n in all_nodes if n.limit is not None)
        for node in all_nodes:
            tree.create_node(
                identifier=node.id,
                tag=node._tree_repr(
                    max_id_suffix_len,
                    max_depth,
                    max_allotment_str_len,
                    max_limit_str_len,
                    max_limit,
                ),
                parent=(node.parent.id if node.parent else None),
            )
        tree.show()

    def _tree_repr(
        self,
        max_id_suffix_len: int,
        max_depth: int,
        max_allotment_str_len: int,
        max_limit_str_len: int,
        max_limit: float,
        indent_per_level: int = 4,
        max_bar_width: int = 50,
    ) -> str:

        def pad(string: str, width: int) -> str:
            return string + " " * (width - len(string))

        repr = (
            pad(self._id_suffix, max_id_suffix_len)
            + " "
            + " " * indent_per_level * (max_depth - self.level)
            + " "
            + f"{pad(f'{self.allotment:.3f}', max_allotment_str_len)}"
        )
        if self.limit is not None:
            repr += f" / {pad(f'{self.limit:.3f}', max_limit_str_len)} "
            barplot = make_ascii_barplot(
                value=self.allotment,
                max_value=self.limit,
                width=int(self.limit / max_limit * max_bar_width),
            )
            repr += f"|{barplot}|"
            return repr
