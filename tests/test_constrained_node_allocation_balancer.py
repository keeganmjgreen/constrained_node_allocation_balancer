import pytest

from constrained_node_allocation_balancer import (
    AncestorChainWithoutLimitError,
    constrained_node_allocation_balancer,
)
from node import Node


def test_raising_if_any_branches_without_limit() -> None:
    with pytest.raises(AncestorChainWithoutLimitError):
        constrained_node_allocation_balancer(Node(limit=None))
    with pytest.raises(AncestorChainWithoutLimitError):
        constrained_node_allocation_balancer(
            Node(limit=None, children=[Node(limit=1), Node(limit=None)])
        )
    with pytest.raises(AncestorChainWithoutLimitError):
        constrained_node_allocation_balancer(
            Node(
                limit=None,
                children=[
                    Node(limit=1),
                    Node(limit=None, children=[Node(limit=1), Node(limit=None)]),
                ],
            )
        )


def test_on_one_level_tree() -> None:
    # Given:
    root = Node(limit=1)
    # When:
    constrained_node_allocation_balancer(root)
    # Then:
    assert root.all_leaf_allotments == {"1": 1}


class TestOnTwoLevelTree:
    @pytest.mark.parametrize("root_limit", [None, 3])
    def test_allocating_to_leaves_without_limiting_parent(
        self, root_limit: float | None
    ) -> None:
        # Given:
        root = Node(
            limit=root_limit,
            children=[
                Node(limit=2),
                Node(limit=1),
            ],
        )
        # When:
        constrained_node_allocation_balancer(root)
        assert root.allotment == 3
        # Then:
        assert root.all_leaf_allotments == {
            "1|1": 2,
            "1|2": 1,
        }

    def test_allocating_to_leaves(self) -> None:
        # Given:
        root = Node(
            limit=2,
            children=[
                Node(limit=2),
                Node(limit=1),
            ],
        )
        # When:
        constrained_node_allocation_balancer(root)
        assert root.allotment == 2
        # Then:
        assert root.all_leaf_allotments == {
            "1|1": 1,
            "1|2": 1,
        }

    def test_allocating_to_leaves_when_redistribution_is_necessary(self) -> None:
        # Given:
        root = Node(
            limit=15,
            children=[
                # These nodes' allotment will start at root.allotment / 3 nodes = 5 units each.
                Node(limit=6),
                # ^ Node 1|1's initial allotment does NOT exceed its limit.
                Node(limit=1),
                # ^ Node 1|2's initial allotment DOES exceed its limit, by 4 units.
                #     This excess will be redistributed among the node's neighbors that have
                #     headroom, allocating 2 more units to each of nodes 1|1 and 1|3.
                #     As a result, node 1|1's allotment will end up exceeding its limit by 1 unit.
                #     This excess will be redistributed among node 1|1's remaining neighbors that
                #     have headroom (in this case, only node 1|3).
                Node(limit=9),
                # ^ Node 1|3's initial allotment does NOT exceed its limit (node has headroom).
            ],
        )
        # When:
        constrained_node_allocation_balancer(root)
        assert root.allotment == 15
        # Then:
        assert root.all_leaf_allotments == {
            "1|1": 6,
            "1|2": 1,
            "1|3": 8,
        }


class TestOnThreeLevelTree:

    def test_allocating_to_leaves_in_proportion_to_n_leaves_at_or_below(self) -> None:
        """Test balancing allocation among leaves regardless of depth."""
        # Given:
        root = Node(
            limit=4,
            children=[
                Node(limit=1),
                Node(
                    children=[
                        Node(limit=2),
                    ]
                ),
                Node(
                    children=[
                        Node(limit=3),
                        Node(limit=4),
                    ]
                ),
            ],
        )
        # When:
        constrained_node_allocation_balancer(root)
        assert root.allotment == 4
        # Then:
        assert root.all_leaf_allotments == {
            "1|1": 1,
            "1|2|1": 1,
            "1|3|1": 1,
            "1|3|2": 1,
        }

    def test_allocating_to_leaves_when_adjusting_inactive_constraint_is_necessary(
        self,
    ) -> None:
        # Given:
        root = Node(
            children=[
                Node(
                    limit=2,  # Inactive constraint; will be adjusted to `1`.
                    children=[Node(limit=1)],
                ),
                Node(
                    limit=9,  # Active constraint.
                    children=[Node(limit=10)],
                ),
            ],
        )
        # When:
        constrained_node_allocation_balancer(root)
        assert root.allotment == 10
        # Then:
        assert root.all_leaf_allotments == {
            "1|1|1": 1,
            "1|2|1": 9,  # Would be `8` without `_adjust_inactive_constraints`.
        }
