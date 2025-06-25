from constrained_node_allocation_balancer import (
    _set_root_allotment,
    constrained_node_allocation_balancer,
)
from node import Node

tree = Node(
    limit=10,
    children=[
        Node(
            limit=5,  # 6,
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
            limit=3,  # 2,
            children=[
                Node(limit=2),
                Node(limit=2),
            ],
        ),
    ],
)
_set_root_allotment(tree)
constrained_node_allocation_balancer(tree, show=False)
tree.show()
