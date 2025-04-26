from __future__ import annotations

import dataclasses
from itertools import groupby

from ete3 import Tree


@dataclasses.dataclass
class Node:
    id: str = dataclasses.field(init=False)
    limit: float | None = None
    children: list[Node] = dataclasses.field(default_factory=list)
    parent: Node | None = dataclasses.field(default=None, repr=False)
    level: int = dataclasses.field(init=False, repr=False)
    allotment: float = 0.0

    def __post_init__(self):
        for child in self.children:
            child.parent = self

    def set_ids(self, starting_id: str = "1") -> None:
        self.id = starting_id
        for i, child in enumerate(self.children):
            child.set_ids(starting_id=f"{self.id}|{i + 1}")

    def set_levels(self, starting_level: int = 0) -> None:
        self.level = starting_level
        for child in self.children:
            child.set_levels(starting_level=(self.level + 1))

    @property
    def remaining_budget(self) -> float:
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
    def ancestor_chain(self) -> list[Node]:
        ancestor_chain: list[Node] = []
        if self.parent is not None:
            ancestor_chain.append(self.parent)
            if self.parent.parent is not None:
                ancestor_chain += self.parent.ancestor_chain
        return ancestor_chain

    @property
    def neighbors(self) -> list[Node]:
        return [n for n in self.parent.nodes_by_level[self.level] if n is not self]

    @property
    def neighbors_with_headroom(self) -> list[Node]:
        return [n for n in self.neighbors if n.has_headroom]

    def as_tree(self) -> Tree:
        tree = Tree()
        attributes = ["id", "limit", "allotment"]
        for attribute in attributes:
            setattr(tree, attribute, getattr(self, attribute))
        for child in self.children:
            tree.add_child(child.as_tree())
        return tree

    def print(self) -> None:
        print(self.as_tree().get_ascii(attributes=["id", "limit", "allotment"]))


def constrained_node_allocation_balancer(tree: Node, show: bool = True) -> None:

    def echo():
        if show:
            tree.print()

    tree.set_ids()
    tree.set_levels()
    echo()
    for leaf in tree.all_leaves:
        leaf.allotment = min(
            n.remaining_budget
            for n in [leaf, *leaf.ancestor_chain]
            if n.limit is not None
        )
        for a in leaf.ancestor_chain:
            a.allotment += leaf.allotment
        if leaf.allotment > 0.0:
            echo()
    for descendent in tree.all_descendents:
        if descendent is not tree:
            descendent.allotment = 0.0
    echo()
    for level, level_nodes in tree.nodes_by_level.items():
        while any(node.limit_exceeded for node in level_nodes):
            for node in level_nodes:
                if node.limit_exceeded:
                    excess = node.allotment - node.limit
                    for neighbor in node.neighbors_with_headroom:
                        neighbor.allotment += (
                            excess
                            / sum(
                                len(neighbor.all_leaves)
                                for neighbor in node.neighbors_with_headroom
                            )
                            * len(neighbor.all_leaves)
                        )
                    node.allotment -= excess
                    echo()
        for node in level_nodes:
            for child in node.children:
                child.allotment = (
                    node.allotment / len(node.all_leaves) * (len(child.all_leaves) or 1)
                )
        echo()


if __name__ == "__main__":
    tree = Node(
        limit=10,
        children=[
            Node(
                limit=5,  # 6
                children=[
                    Node(
                        limit=3,
                        children=[
                            Node(limit=2),
                            Node(limit=2),
                        ],
                    ),
                    Node(
                        limit=3,
                        children=[
                            Node(limit=2),
                            Node(limit=2),
                        ],
                    ),
                ],
            ),
            Node(
                limit=3,
                children=[
                    Node(limit=2),
                    Node(limit=2),
                ],
            ),
            Node(
                limit=3,  # 2
                children=[
                    Node(limit=2),
                    Node(limit=2),
                ],
            ),
        ],
    )
    constrained_node_allocation_balancer(tree, show=False)
    tree.print()
