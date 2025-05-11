import pytest

from constrained_node_allocation_balancer import (
    constrained_node_allocation_balancer,
    remove_inactive_constraints,
    set_root_allotment,
)
from node import Node


class TestOnSimpleTwoLevelTree:
    @pytest.mark.parametrize("root_limit", [None, 3])
    def test_allocating_to_leaves_without_limiting_parent(
        self, root_limit: float | None
    ):
        # Given:
        root = Node(
            limit=root_limit,
            children=[
                Node(limit=2),
                Node(limit=1),
            ],
        )
        set_root_allotment(root)
        assert root.allotment == 3
        remove_inactive_constraints(root)
        # When:
        constrained_node_allocation_balancer(root)
        # Then:
        assert root.all_leaf_allotments == {
            "1|1": 2,
            "1|2": 1,
        }

    def test_allocating_to_leaves(self):
        # Given:
        root = Node(
            limit=2,
            children=[
                Node(limit=2),
                Node(limit=1),
            ],
        )
        set_root_allotment(root)
        assert root.allotment == 2
        remove_inactive_constraints(root)
        # When:
        constrained_node_allocation_balancer(root)
        # Then:
        assert root.all_leaf_allotments == {
            "1|1": 1,
            "1|2": 1,
        }

    def test_allocating_to_leaves_when_redistribution_is_necessary(self):
        # Given:
        root = Node(
            limit=6,
            children=[
                # These nodes' allotment will start at root.allotment / 3 nodes = 2 units each.
                Node(limit=2),
                # ^ Node 1|1's initial allotment does NOT exceed its limit.
                Node(limit=1),
                # ^ Node 1|2's initial allotment DOES exceed its limit, by 1 unit.
                #     This excess will be redistributed among the node's neighbors that have headroom,
                #     allocating 0.5 more units to each of nodes 1|1 and 1|3.
                #     As a result, node 1|1's allotment will end up exceeding its limit by 0.5 units.
                #     This excess will be redistributed among node 1|1's remaining neighbors that have
                #     headroom (in this case, only node 1|3).
                Node(limit=4),
                # ^ Node 1|3's initial allotment does NOT exceed its limit (node has headroom).
            ],
        )
        set_root_allotment(root)
        assert root.allotment == 6
        remove_inactive_constraints(root)
        # When:
        constrained_node_allocation_balancer(root)
        # Then:
        assert root.all_leaf_allotments == {
            "1|1": 2,
            "1|2": 1,
            "1|3": 3,
        }


class TestOnThreeLevelTree:

    def test_(self):
        # Given:
        root = Node(
            children=[
                Node(limit=2, children=[Node(limit=1)]),
                Node(limit=9, children=[Node(limit=10)]),
            ],
        )
        set_root_allotment(root)
        assert root.allotment == 10
        remove_inactive_constraints(root)
        # When:
        remove_inactive_constraints(root)
        constrained_node_allocation_balancer(root)
        # Then:
        assert root.all_leaf_allotments == {
            "1|1": 2,
            "1|2": 1,
        }
