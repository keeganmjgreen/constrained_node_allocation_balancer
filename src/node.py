from __future__ import annotations

import math
from itertools import groupby
from typing import Any, Literal, override

import python_to_mermaid

from ascii_barplot import make_ascii_barplot, make_ascii_barplot_with_marker
from utils import pad


class Node:
    id: str
    _id_suffix: str
    limit: float = float("inf")
    children: list[Node]
    parent: Node | None
    level: int
    allocation: float

    def __init__(self, children: list[Node], limit: float = float("inf")):
        self.limit = limit
        self.children = children
        if len(self.children) == 0:
            raise ValueError(
                "A non-leaf Node must have one or more children. Otherwise, use LeafNode."
            )
        for child in self.children:
            child.parent = self
        self.parent = None
        # Set IDs and levels, assuming (for now) that this is the root node:
        self._set_ids()
        self._set_levels()
        self.allocation = 0.0

    def _set_ids(self, starting_at: str = "1", separator: str = ".") -> None:
        self._id_suffix = starting_at
        if self.parent is None:
            self.id = self._id_suffix
        else:
            self.id = self.parent.id + separator + self._id_suffix
        for i, child in enumerate(self.children):
            child._set_ids(starting_at=str(i + 1))

    def _set_levels(self, starting_level: int = 0) -> None:
        self.level = starting_level
        for child in self.children:
            child._set_levels(starting_level=(self.level + 1))

    # ==============================================================================================
    # Methods comparing the node's allocation to its limit:

    @property
    def remaining_budget(self) -> float:
        return self.limit - self.allocation

    @property
    def limit_exceeded(self) -> bool:
        return self.allocation > self.limit

    @property
    def has_headroom(self) -> bool:
        return self.allocation < self.limit

    # ==============================================================================================
    # Methods concerning the structure of the tree:

    @property
    def all_descendants(self) -> list[Node]:
        """Return a list of all the node's children, those children's children, and so on, until
        leaf nodes are reached, in depth-first order.
        """
        descendants: list[Node] = []
        for child in self.children:
            descendants.append(child)
            descendants += child.all_descendants
        return descendants

    @property
    def all_nodes(self) -> list[Node]:
        """Return a list of all the tree's nodes, in depth-first order."""
        return [self, *self.all_descendants]

    @property
    def nodes_by_level(self) -> dict[int, list[Node]]:
        """Return a list of nodes for each level in the tree."""
        return {
            k: list(g)
            for k, g in groupby(
                sorted(self.all_nodes, key=(lambda node: node.level)),
                key=(lambda node: node.level),
            )
        }

    @property
    def siblings(self) -> list[Node] | None:
        """If the node is not the root node, return a list of nodes sharing the same parent."""
        if self.parent is not None:
            return [n for n in self.parent.nodes_by_level[self.level] if n is not self]

    @property
    def siblings_with_headroom(self) -> list[Node] | None:
        if self.parent is not None:
            return [n for n in self.siblings if n.has_headroom]

    @property
    def ancestor_chain(self) -> list[Node]:
        """Return a list containing the node's parent, grandparent, and so on until the root node."""
        ancestor_chain: list[Node] = []
        if self.parent is not None:
            ancestor_chain.append(self.parent)
            if self.parent.parent is not None:
                ancestor_chain += self.parent.ancestor_chain
        return ancestor_chain

    # ----------------------------------------------------------------------------------------------
    # Methods concerning leaf nodes:

    @property
    def all_leaves(self) -> list[LeafNode]:
        leaves: list[LeafNode] = []
        for child in self.children:
            leaves += child.all_leaves
        return leaves

    @property
    def n_leaves_at_or_below(self) -> float:
        """Return the number of leaves under the node, or 1 if the node is a leaf.

        If there are non-1.0 conversion factors, this returns the number of leaves adjusted by their
        conversion factors.
        """

        return sum(leaf.conversion_factor for leaf in self.all_leaves)

    @property
    def sum_of_shift_constants_at_or_below(self) -> float:
        return sum(leaf.shift_constant for leaf in self.all_leaves)

    @property
    def all_leaf_allocations(self) -> dict[str, float]:
        return {leaf.id: leaf.allocation for leaf in self.all_leaves}

    # ==============================================================================================
    # Methods for tree visualization:

    def show(
        self,
        max_allocation_str_len: int | None = None,
        max_limit_str_len: int | None = None,
        max_value: float | None = None,
        how: Literal["ascii", "mermaid"] = "ascii",
    ) -> None:
        print(self.tree_repr(max_allocation_str_len, max_limit_str_len, max_value, how))

    def tree_repr(
        self,
        max_allocation_str_len: int | None = None,
        max_limit_str_len: int | None = None,
        max_value: float | None = None,
        how: Literal["ascii", "mermaid"] = "ascii",
        max_bar_width: int | None = None,
    ) -> str:
        all_nodes = self.all_nodes
        max_allocation = max(n.allocation for n in all_nodes)
        if max_allocation_str_len is None:
            max_allocation_str_len = len(f"{max_allocation:.3f}")
        max_limit = max(n.limit for n in all_nodes if not math.isinf(n.limit))
        if max_limit_str_len is None:
            max_limit_str_len = len(f"{max_limit:.3f}")
        if max_value is None:
            max_value = max(max_allocation, max_limit)
        if max_bar_width is None:
            max_bar_width = {"ascii": 50, "mermaid": 10}[how]

        if how == "ascii":
            return self._tree_repr(
                max_id_suffix_len=max(len(n._id_suffix) for n in all_nodes),
                max_depth=max(n.level for n in all_nodes),
                max_allocation_str_len=max_allocation_str_len,
                max_limit_str_len=max_limit_str_len,
                max_value=max_value,
                max_bar_width=max_bar_width,
            )
        elif how == "mermaid":
            diagram = python_to_mermaid.MermaidDiagram()
            for node in all_nodes:
                diagram.add_node(
                    node.id,
                    label=(
                        f"<b>{node.id}</b>"
                        + "<br>"
                        + f"{node.allocation:.3f}"
                        + ("" if math.isinf(node.limit) else f" / {node.limit:.3f}")
                        + "<br>"
                        + f"<code>{node._ascii_barplot(max_value, max_bar_width, blank=".")}</code>"
                    ),
                )
                if node.parent is not None:
                    diagram.add_edge(node.parent.id, node.id)
            return str(diagram)
        else:
            raise NotImplementedError

    def _tree_repr(
        self,
        max_id_suffix_len: int,
        max_depth: int,
        max_allocation_str_len: int,
        max_limit_str_len: int,
        indent_per_level: int = 4,
        root: bool = True,
        header: str = "",
        last: bool = True,
        **node_repr_kwargs: dict[str, Any],
    ) -> str:
        elbow = "└───"
        pipe = "│   "
        tee = "├───"
        blank = "    "
        text = (
            ("" if root else "\n")
            + header
            + ("" if root else elbow if last else tee)
            + pad(self._id_suffix, max_id_suffix_len)
            + " "
            + " " * indent_per_level * (max_depth - self.level)
            + f"{pad(f'{self.allocation:.3f}', max_allocation_str_len)}"
            + (
                " " * (4 + max_limit_str_len)
                if math.isinf(self.limit)
                else f" / {pad(f'{self.limit:.3f}', max_limit_str_len)} "
            )
            + self._ascii_barplot(**node_repr_kwargs)
        )
        for i, child in enumerate(self.children):
            text += child._tree_repr(
                max_id_suffix_len,
                max_depth,
                max_allocation_str_len,
                max_limit_str_len,
                indent_per_level,
                root=False,
                header=(header + ("" if root else blank if last else pipe)),
                last=(i == len(self.children) - 1),
                **node_repr_kwargs,
            )
        return text

    def _ascii_barplot(
        self, max_value: float, max_bar_width: int, blank: str = " "
    ) -> str:
        if math.isinf(self.limit):
            barplot = make_ascii_barplot(
                value=self.allocation,
                max_value=max_value,
                width=max_bar_width,
                blank=blank,
            )
        else:
            barplot = make_ascii_barplot_with_marker(
                value=self.allocation,
                marker=self.limit,
                max_value=max_value,
                width=max_bar_width,
                blank=blank,
            )
        return f"|{barplot}"


class LeafNode(Node):
    conversion_factor: float
    shift_constant: float

    @override
    def __init__(
        self,
        limit: float = float("inf"),
        conversion_factor: float = 1.0,
        shift_constant: float = 0.0,
    ):
        """Create a leaf node

        Args:
            limit (float, optional): Limit. Defaults to float("inf").
            conversion_factor (float, optional): A factor by which to multiply the units of the
                allocation to convert to the units of the limit. Defaults to 1.0.
            shift_constant (float, optional): A constant to subtract from the allocation of a parent
                before distributing among its children, after which the constant is added again.
                Defaults to 0.0.
        """

        self.limit = limit
        self.parent = None
        self.children = []
        # Set IDs and levels, assuming (for now) that this is the root node:
        self._set_ids()
        self._set_levels()
        self.allocation = 0.0
        self.conversion_factor = conversion_factor
        self.shift_constant = shift_constant

    @override
    @property
    def all_leaves(self) -> list[LeafNode]:
        return [self]

    @override
    @property
    def remaining_budget(self) -> float:
        return self.limit - self.allocation * self.conversion_factor

    @override
    @property
    def limit_exceeded(self) -> bool:
        return self.allocation * self.conversion_factor > self.limit

    @override
    @property
    def has_headroom(self) -> bool:
        return self.allocation * self.conversion_factor < self.limit
