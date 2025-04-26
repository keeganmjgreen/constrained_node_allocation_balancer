import pytest

from src.constrained_node_allocation_balancer import (
    Node,
    constrained_node_allocation_balancer,
    set_root_allocation,
)


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
            is_root=True,
        )
        set_root_allocation(root)
        assert root.allotment == 3
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
            is_root=True,
        )
        set_root_allocation(root)
        assert root.allotment == 2
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
                # ^ Node 1|1's initial allotment does NOT exceed its limit (node has headroom).
                Node(limit=1),
                # ^ Node 1|2's initial allotment DOES exceed its limit by 1 unit.
                #     This excess will be redistributed among the node's neighbors that have headroom,
                #     allocating 0.5 more units to each of nodes 1|1 and 1|3.
                #     As a result, node 1|1's allotment will end up exceeding its limit by 0.5 units.
                #     This excess will be redistributed among node 1|1's remaining neighbors that have
                #     headroom (in this case, only node 1|3).
                Node(limit=4),
                # ^ Node 1|3's initial allotment does NOT exceed its limit (node has headroom).
            ],
            is_root=True,
        )
        set_root_allocation(root)
        assert root.allotment == 6
        # When:
        constrained_node_allocation_balancer(root)
        # Then:
        assert root.all_leaf_allotments == {
            "1|1": 2,
            "1|2": 1,
            "1|3": 3,
        }


class TestOnThreeLevelTree:
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
            is_root=True,
        )
        set_root_allocation(root)
        assert root.allotment == 3
        # When:
        constrained_node_allocation_balancer(root)
        # Then:
        assert root.all_leaf_allotments == {
            "1|1": 2,
            "1|2": 1,
        }
