import math
from typing import Callable

from logs import Logs
from node import Node


def constrained_node_allocation_balancer(tree: Node, return_logs: bool = False) -> None:
    logs = Logs()

    def logger(message: str, tree: Node):
        if return_logs:
            logs.add(message, tree)

    _set_root_allocation(tree, logger)
    _adjust_inactive_limits(tree, logger)
    _balance_allocations(tree, logger)

    if return_logs:
        return logs


def _set_root_allocation(tree: Node, logger: Callable) -> None:
    for node in tree.all_nodes:
        if node.allocation != 0.0:
            raise ValueError("All node allocations must start at 0.0.")
    for leaf in tree.all_leaves:
        ancestral_budgets = [
            n.remaining_budget
            for n in [leaf, *leaf.ancestor_chain]
            if not math.isinf(n.limit)
        ]
        if len(ancestral_budgets) == 0:
            raise AncestorChainWithoutLimitError
        leaf.allocation = min(ancestral_budgets)
        for a in leaf.ancestor_chain:
            a.allocation += leaf.allocation
        logger(f"Allocated {min(ancestral_budgets) = } to leaf {leaf.id}", tree)
    for descendant in tree.all_descendants:
        descendant.allocation = 0.0
    logger("Cleared allocations from all non-root nodes", tree)


def _adjust_inactive_limits(tree: Node, logger: Callable) -> None:
    for level, level_nodes in reversed(tree.nodes_by_level.items()):  # Root last.
        if level == 0:
            continue
        for node in level_nodes:
            children_throughput = sum(n.limit for n in node.children)
            if len(node.children) > 0 and (
                math.isinf(node.limit) or children_throughput <= node.limit
            ):
                # The node has no limit, or the node's limit can never be reached due to its
                #     children's limits. Set the node's limit to the sum of its children's limits:
                node.limit = children_throughput
                logger(
                    f"Set limit of node {node.id} to the sum of its children's limits "
                    f"{children_throughput}",
                    tree,
                )


def _balance_allocations(tree: Node, logger: Callable) -> None:
    for level_nodes in tree.nodes_by_level.values():
        # Redistribute nodes' allocations until all nodes' limits are respected:
        while any(node.limit_exceeded for node in level_nodes):
            for node in level_nodes:
                if node.limit_exceeded:
                    excess = node.allocation - node.limit
                    siblings_with_headroom = node.siblings_with_headroom
                    for sibling in siblings_with_headroom:
                        sibling.allocation += (
                            (
                                excess
                                - sum(
                                    sibling.sum_of_shift_constants_at_or_below
                                    for sibling in siblings_with_headroom
                                )
                            )
                            / sum(
                                sibling.n_leaves_at_or_below
                                for sibling in siblings_with_headroom
                            )
                            * sibling.n_leaves_at_or_below
                        ) + sibling.sum_of_shift_constants_at_or_below
                    node.allocation -= excess
                    logger(
                        f"Redistributed {excess} from node {node.id} to siblings with headroom "
                        f"{[s.id for s in siblings_with_headroom]}",
                        tree,
                    )
        for node in level_nodes:
            for child in node.children:
                child.allocation = (
                    (node.allocation - node.sum_of_shift_constants_at_or_below)
                    / node.n_leaves_at_or_below
                    * child.n_leaves_at_or_below
                ) + child.sum_of_shift_constants_at_or_below
            if len(node.children) > 0:
                logger(
                    f"Distributed {node.allocation} from node {node.id} to children "
                    f"{[c.id for c in node.children]}",
                    tree,
                )


class AncestorChainWithoutLimitError(Exception):
    pass
