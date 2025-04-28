from node import Node


def set_root_allotment(tree: Node) -> None:
    for leaf in tree.all_leaves:
        leaf.allotment = min(
            n.remaining_budget
            for n in [leaf, *leaf.ancestor_chain]
            if n.limit is not None
        )
        for a in leaf.ancestor_chain:
            a.allotment += leaf.allotment
    for descendent in tree.all_descendents:
        if descendent is not tree:
            descendent.allotment = 0.0


def remove_inactive_constraints(tree: Node) -> None:
    pass


def constrained_node_allocation_balancer(tree: Node, show: bool = True) -> None:
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
                    for neighbor in node.neighbors_with_headroom:
                        neighbor.allotment += (
                            excess
                            / sum(
                                neighbor.n_leaves_at_or_below
                                for neighbor in node.neighbors_with_headroom
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
