import pytest

from constrained_node_allocation_balancer import (
    AncestorChainWithoutLimitError,
    Logs,
    constrained_node_allocation_balancer,
)
from node import LeafNode, Node


def test_raising_if_any_branches_without_limit() -> None:
    with pytest.raises(AncestorChainWithoutLimitError):
        constrained_node_allocation_balancer(LeafNode(limit=float("inf")))
    with pytest.raises(AncestorChainWithoutLimitError):
        constrained_node_allocation_balancer(
            Node(
                limit=float("inf"),
                children=[LeafNode(limit=1), LeafNode(limit=float("inf"))],
            )
        )
    with pytest.raises(AncestorChainWithoutLimitError):
        constrained_node_allocation_balancer(
            Node(
                limit=float("inf"),
                children=[
                    LeafNode(limit=1),
                    Node(
                        limit=float("inf"),
                        children=[LeafNode(limit=1), LeafNode(limit=float("inf"))],
                    ),
                ],
            )
        )


def test_on_one_level_tree() -> None:
    # Given:
    root = LeafNode(limit=1)
    # When:
    constrained_node_allocation_balancer(root)
    # Then:
    assert root.all_leaf_allocations == {"1": 1}


class TestOnTwoLevelTree:

    @pytest.mark.parametrize("root_limit", [float("inf"), 3])
    def test_allocating_to_leaves_without_limiting_parent(
        self, root_limit: float
    ) -> None:
        # Given:
        root = Node(
            limit=root_limit,
            children=[
                LeafNode(limit=2),
                LeafNode(limit=1),
            ],
        )
        # When:
        logs: Logs = constrained_node_allocation_balancer(root, return_logs=True)
        assert root.allocation == 3
        logs.show()
        logs.write(
            "tests/diagrams/test_allocating_to_leaves_without_limiting_parent.md"
        )
        # Then:
        assert root.all_leaf_allocations == {
            "1.1": 2,
            "1.2": 1,
        }

    def test_allocating_to_leaves_without_limits(self) -> None:
        # Given:
        root = Node(
            limit=2,
            children=[
                LeafNode(limit=float("inf")),
                LeafNode(limit=float("inf")),
            ],
        )
        # When:
        logs: Logs = constrained_node_allocation_balancer(root, return_logs=True)
        assert root.allocation == 2
        logs.show()
        logs.write("tests/diagrams/test_allocating_to_leaves_without_limits.md")
        # Then:
        assert root.all_leaf_allocations == {
            "1.1": 1,
            "1.2": 1,
        }

    def test_allocating_to_leaves(self) -> None:
        # Given:
        root = Node(
            limit=2,
            children=[
                LeafNode(limit=2),
                LeafNode(limit=1),
            ],
        )
        # When:
        logs: Logs = constrained_node_allocation_balancer(root, return_logs=True)
        assert root.allocation == 2
        logs.show()
        logs.write("tests/diagrams/test_allocating_to_leaves.md")
        # Then:
        assert root.all_leaf_allocations == {
            "1.1": 1,
            "1.2": 1,
        }

    def test_allocating_to_leaves_when_redistribution_is_necessary(self) -> None:
        # Given:
        root = Node(
            limit=15,
            children=[
                # These nodes' allocations will start at root.allocation / 3 nodes = 5 units each.
                LeafNode(limit=6),
                # ^ Node 1.1's initial allocation does NOT exceed its limit.
                LeafNode(limit=1),
                # ^ Node 1.2's initial allocation DOES exceed its limit, by 4.0 units.
                #     This excess will be redistributed among the node's siblings that have
                #     headroom, allocating 2.0 more units to each of nodes 1.1 and 1.3.
                #     As a result, node 1.1's allocation will end up exceeding its limit by 1.0
                #     unit.
                #     This excess will be redistributed among node 1.1's remaining siblings that
                #     have headroom (in this case, only node 1.3).
                LeafNode(limit=9),
                # ^ Node 1.3's initial allocation does NOT exceed its limit (node has headroom).
            ],
        )
        # When:
        logs: Logs = constrained_node_allocation_balancer(root, return_logs=True)
        assert root.allocation == 15
        logs.show()
        logs.write(
            "tests/diagrams/test_allocating_to_leaves_when_redistribution_is_necessary.md"
        )
        # Then:
        assert root.all_leaf_allocations == {
            "1.1": 6,
            "1.2": 1,
            "1.3": 8,
        }


class TestOnThreeLevelTree:

    def test_allocating_to_leaves_when_redistribution_is_necessary_2(self) -> None:
        """This would fail if `.siblings` were replaced with `.neighbors`
        (siblings, cousins, and so on).
        """
        # Given:
        root = Node(
            children=[
                Node(
                    children=[
                        LeafNode(limit=1),
                        LeafNode(limit=2),
                    ],
                ),
                Node(
                    limit=2,
                    children=[
                        LeafNode(limit=1),
                        LeafNode(limit=2),
                    ],
                ),
            ],
        )
        # When:
        logs: Logs = constrained_node_allocation_balancer(root, return_logs=True)
        assert root.allocation == 5
        logs.show()
        logs.write(
            "tests/diagrams/test_allocating_to_leaves_when_redistribution_is_necessary_2.md"
        )
        # Then:
        assert root.all_leaf_allocations == {
            "1.1.1": 1,  # Would be `1.00` with `.neighbors` instead of `.siblings`.
            "1.1.2": 2,  # Would be `1.75` with `.neighbors` instead of `.siblings`.
            "1.2.1": 1,  # Would be `1.00` with `.neighbors` instead of `.siblings`.
            "1.2.2": 1,  # Would be `1.25` with `.neighbors` instead of `.siblings`.
        }

    def test_allocating_to_leaves_in_proportion_to_n_leaves_at_or_below(self) -> None:
        """Test balancing allocation among leaves regardless of depth."""
        # Given:
        root = Node(
            limit=4,
            children=[
                LeafNode(limit=1),
                Node(
                    children=[
                        LeafNode(limit=2),
                    ]
                ),
                Node(
                    children=[
                        LeafNode(limit=3),
                        LeafNode(limit=4),
                    ]
                ),
            ],
        )
        # When:
        logs: Logs = constrained_node_allocation_balancer(root, return_logs=True)
        assert root.allocation == 4
        logs.show()
        logs.write(
            "tests/diagrams/test_allocating_to_leaves_in_proportion_to_n_leaves_at_or_below.md"
        )
        # Then:
        assert root.all_leaf_allocations == {
            "1.1": 1,
            "1.2.1": 1,
            "1.3.1": 1,
            "1.3.2": 1,
        }

    def test_reallocating_to_leaves_in_proportion_to_n_leaves_at_or_below(self) -> None:
        # Given:
        root = Node(
            children=[
                LeafNode(limit=1),
                Node(
                    children=[
                        LeafNode(limit=2),
                    ]
                ),
                Node(
                    children=[
                        LeafNode(limit=3),
                        LeafNode(limit=4),
                    ]
                ),
            ],
        )
        # When:
        logs: Logs = constrained_node_allocation_balancer(root, return_logs=True)
        assert root.allocation == 10
        logs.show()
        logs.write(
            "tests/diagrams/test_reallocating_to_leaves_in_proportion_to_n_leaves_at_or_below.md"
        )
        # Then:
        assert root.all_leaf_allocations == {
            "1.1": 1,
            "1.2.1": 2,
            "1.3.1": 3,
            "1.3.2": 4,
        }

    def test_allocating_to_leaves_when_adjusting_inactive_limit_is_necessary(
        self,
    ) -> None:
        # Given:
        root = Node(
            children=[
                Node(
                    limit=20,  # Inactive limit; will be adjusted to `10`.
                    children=[LeafNode(limit=10)],
                ),
                Node(
                    limit=80,  # Active limit.
                    children=[LeafNode(limit=100)],
                ),
            ],
        )
        # When:
        logs: Logs = constrained_node_allocation_balancer(root, return_logs=True)
        assert root.allocation == 90
        logs.show()
        logs.write(
            "tests/diagrams/test_allocating_to_leaves_when_adjusting_inactive_limit_is_necessary.md"
        )
        # Then:
        assert root.all_leaf_allocations == {
            "1.1.1": 10,
            "1.2.1": 80,  # Would be `70` without `_adjust_inactive_limits`.
        }


class TestOnFourLevelTree:

    def test_allocating_to_leaves_when_adjusting_inactive_limits_is_necessary(
        self,
    ) -> None:
        # Given:
        root = Node(
            children=[
                Node(
                    limit=20,  # Inactive limit; will be adjusted to `10`.
                    children=[
                        Node(
                            limit=2,  # Inactive limit; will be adjusted to `1`.
                            children=[LeafNode(limit=1)],
                        ),
                        Node(
                            limit=8,  # Active limit.
                            children=[LeafNode(limit=10)],
                        ),
                    ],
                ),
                Node(
                    limit=80,  # Active limit.
                    children=[LeafNode(limit=100)],
                ),
            ],
        )
        # When:
        logs: Logs = constrained_node_allocation_balancer(root, return_logs=True)
        assert root.allocation == 89
        logs.show()
        logs.write(
            "tests/diagrams/test_allocating_to_leaves_when_adjusting_inactive_limits_is_necessary.md"
        )
        # Then:
        assert root.all_leaf_allocations == {
            "1.1.1.1": 1,
            "1.1.2.1": 8,
            "1.2.1": 80,  # Would be `70` without `_adjust_inactive_limits`.
        }
