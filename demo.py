from constrained_node_allocation_balancer import (
    Logs,
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
logs: Logs = constrained_node_allocation_balancer(tree, return_logs=True)
logs.show()
