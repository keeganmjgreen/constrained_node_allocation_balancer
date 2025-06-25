from node import Node


def constrained_node_allocation_balancer(tree: Node, show: bool = True) -> None:
    _set_root_allotment(tree)
    _adjust_inactive_constraints(tree)
    _balance_allocations(tree, show)


def _set_root_allotment(tree: Node) -> None:
    for leaf in tree.all_leaves:
        ancestral_budgets = [
            n.remaining_budget
            for n in [leaf, *leaf.ancestor_chain]
            if n.limit is not None
        ]
        if len(ancestral_budgets) == 0:
            raise AncestorChainWithoutLimitError
        leaf.allotment = min(ancestral_budgets)
        for a in leaf.ancestor_chain:
            a.allotment += leaf.allotment
    for descendant in tree.all_descendants:
        if descendant is not tree:
            descendant.allotment = 0.0


def _adjust_inactive_constraints(tree: Node) -> None:
    for level_nodes in reversed(tree.nodes_by_level.values()):  # Root first.
        for node in level_nodes:
            if len(node.children) > 0 and (
                node.limit is None or sum(n.limit for n in node.children) <= node.limit
            ):
                # The node has no limit, or the node's limit can never be reached due to its
                #     children's limits. Set the node's limit to the sum of its children's limits:
                node.limit = sum(n.limit for n in node.children)


def _balance_allocations(tree: Node, show: bool = True) -> None:
    assert tree.allotment is not None

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
