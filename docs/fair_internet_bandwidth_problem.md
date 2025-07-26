# Application: The 'Fair Internet Bandwidth' Problem

Consider an internet network structured as a tree, in which the root node is the only producer of of data and the leaves are the only consumers of data. The direction of data flow is exclusively from root to leaves. This is not a terrible model for a lot of internet traffic, for example media streaming services, in which the root represents streaming services' servers in one region, and the leaves represent the users of those streaming services. Users upload a negligible amount of data compared to how much they download. Each user requests data transfer at a speed up to the maximum speed of the internet service plan they pay for. In the tree-like network, the intermediate nodes (between the root and leaves) represent the internet infrastructure and data transfer speed limits imposed by it (fiber versus cable versus fixed internet).

The 'fair internet bandwidth' problem asks how to distribute internet bandwidth fairly among users that are requesting data at different speeds, with different maximum speeds according to their internet service plans, in service areas that differ in terms of internet infrastructure.

The following example shows how the 'fair internet bandwidth' problem can be solved using the Constrained Node Allocation Balancer package. A subclass of `Node` called `InternetUser` is created, defining the node's `limit` as the lesser of the user's maximum speed (per their internet service plan) and their requested speed. The algorithm evenly distributes bandwidth among users until a limit is reached---whether that of the data transfer speed being requested by a customer, or the maximum speed for a user, or of the upstream infrastructure. At this point, the algorithm redistributes excess bandwidth as fairly as possible. The algorithm would be re-executed constantly to account for users' constantly fluctuating data needs.

```python
import dataclasses

from constrained_node_allocation_balancer import Node


@dataclasses.dataclass
class InternetUser(Node):
    requested_speed_mbps: float
    max_speed_mbps: float = float("inf")

    @property
    def limit(self) -> float:
        return min(self.max_speed_mbps, self.requested_speed_mbps)


streaming_service_1 := Node(
    children=[
        switch_1 := Node(
            limit=4,
            children=[
                user_1 := InternetUser(max_speed=2, requested_speed=4),
                user_2 := InternetUser(max_speed=3, requested_speed=3),
            ],
        ),
        switch_2 := Node(
            limit=4,
            children=[
                user_3 := InternetUser(max_speed=4, requested_speed=2),
                user_4 := InternetUser(max_speed=5, requested_speed=1),
            ],
        ),
    ]
)
constrained_node_allocation_balancer(streaming_service_1)
user_1.allocation  # 2.0
user_2.allocation  # 2.0
user_3.allocation  # 2.0
user_4.allocation  # 1.0
```

## Variant: balancing the fraction of requested speed that is fulfilled

In a variant of the fair internet bandwidth problem, the question is not of how to fairly distribute internet bandwidth, but how to fairly distribute the fraction of each user's requested data transfer speed that is fulfilled. Obviously, it is theoretically possible that all users' data transfer speeds can be fulfilled, but this trivial case is not true in general.

This variant focuses more than the original problem on delivering internet speeds that are in proportion to how much users pay. The variant would be a fairer approach than the original formulation if users paid a fixed monthly cost per Mbps, however rural users obviously pay more per Mbps per month than urban users (and depending on their monthly Mb limit, for that matter).

The `InternetUser` subclass of `Node` is changed to the following to solve the variant, now defining a `conversion_factor` for the node. This conversion factor is a feature of the Constrained Node Allocation Balancer algorithm which allows different units to be used for their `limit` and `allocation`, for all nodes. In this case, the `limit` is in Mbps and the `allocation` is dimensionless (a fraction between 0 and 1).

```python
@dataclasses.dataclass
class InternetUser(Node):
    requested_speed_mbps: float
    max_speed_mbps: float = float("inf")

    @property
    def limit(self) -> float:
        return min(self.max_speed_mbps, self requested_speed_mbps)

    @property
    def conversion_factor(self) -> float:
        return self.limit
```
