from constrained_node_allocation_balancer import (
    constrained_node_allocation_balancer,
    set_root_allotment,
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
set_root_allotment(tree)
constrained_node_allocation_balancer(tree, show=False)
tree.show()
