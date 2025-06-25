import math

from node import Node


def constrained_node_allocation_balancer(tree: Node, show: bool = True) -> None:
    _set_root_allotment(tree)
    _adjust_inactive_limits(tree)
    _balance_allocations(tree, show)


def _set_root_allotment(tree: Node) -> None:
    for node in tree.all_nodes:
        if node.allotment != 0.0:
            raise ValueError("All node allotments must start at 0.0.")
    for leaf in tree.all_leaves:
        ancestral_budgets = [
            n.remaining_budget
            for n in [leaf, *leaf.ancestor_chain]
            if not math.isinf(n.limit)
        ]
        if len(ancestral_budgets) == 0:
            raise AncestorChainWithoutLimitError
        leaf.allotment = min(ancestral_budgets)
        for a in leaf.ancestor_chain:
            a.allotment += leaf.allotment
    for descendant in tree.all_descendants:
        descendant.allotment = 0.0


def _adjust_inactive_limits(tree: Node) -> None:
    for level_nodes in reversed(tree.nodes_by_level.values()):  # Root last.
        for node in level_nodes:
            children_throughput = sum(n.limit for n in node.children)
            if len(node.children) > 0 and (
                math.isinf(node.limit) or children_throughput <= node.limit
            ):
                # The node has no limit, or the node's limit can never be reached due to its
                #     children's limits. Set the node's limit to the sum of its children's limits:
                node.limit = children_throughput


def _balance_allocations(tree: Node, show: bool = True) -> None:
    def echo():
        if show:
            tree.show()

    echo()
    for level_nodes in tree.nodes_by_level.values():
        # Redistribute nodes' allotments until all nodes' limits are respected:
        while any(node.limit_exceeded for node in level_nodes):
            for node in level_nodes:
                if node.limit_exceeded:
                    excess = node.allotment - node.limit
                    neighbors_with_headroom = node.neighbors_with_headroom
                    for neighbor in neighbors_with_headroom:
                        neighbor.allotment += (
                            excess
                            / sum(
                                neighbor.n_leaves_at_or_below
                                for neighbor in neighbors_with_headroom
                            )
                            * neighbor.n_leaves_at_or_below
                        )
                    node.allotment -= excess
                    echo()
        for node in level_nodes:
            for child in node.children:
                child.allotment = (
                    node.allotment
                    / node.n_leaves_at_or_below
                    * child.n_leaves_at_or_below
                )
        echo()


class AncestorChainWithoutLimitError(Exception):
    pass
