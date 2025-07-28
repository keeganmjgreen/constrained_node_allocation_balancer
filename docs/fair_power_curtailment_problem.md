# Application: The 'Fair Power Curtailment' Problem

The electrical grid is a complex system ranging from generation and transmission to distribution and final consumption. While increases in consumer "behind-the-meter" rooftop solar panels have reduced strain on the grid and started to change the status quo of who in the grid can produce energy, the vast majority of electricity still comes from centralized power plants and wind or solar farms. On the other hand, the past decade has seen remarkable adoption of EVs, the charging of which threatens to increase strain on the grid---both in terms of how well existing generation can meet the increased demand, and in terms of how well existing grid infrastructure can handle that extra power.

A better solution than solely increasing generation and infrastructure capacity is to intelligently manage EV charging at grid scale, curtailing or shifting EV charging to avoid peaks and smooth out the load. The question remains of how much to curtail, and where. This depends on where there exist limited capacities, in terms of generation, transformers, and distribution lines, in the grid.

The Constrained Node Allocation Balancer algorithm can be used to solve this problem by modeling the grid as a tree consisting of limits. The tree's root node represents the centralized generation of power, the leaf nodes represent the final consumers of electricity, and the intermediate nodes represent transmission and distribution. The nodes' limits represent limited generation capacity, power limits imposed by transformers and distribution lines, and the finite amount of power that each grid user wants to use at any given time. Power flow is generally unidirectional, from the top down, but in general can be bidirectional in our tree model, which accounts for behind-the-meter solar and even net grid export from solar producers.

```python
import dataclasses

from constrained_node_allocation_balancer import LeafNode, Range


@dataclasses.dataclass
class GridUser(LeafNode):
    fixed_net_load_kw: float
    dispatchable_generation: float
    dispatchable_load: float

    @property
    def limits(self) -> Range:
        return Range(
            lower=self.dispatchable_generation,
            upper=self.dispatchable_load,
        )

        @property
    def shift_constant(self) -> float:
        return self.fixed_net_load_kw


centralized_generation := Node(
    upper_limit=sum(
        power_plant_output_kw,
        solar_farm_output_kw,
        wind_farm_output_kw,
    ),
    children=[
        feeder_transformer_1 := Node(
            upper_limit=4,
            children=[
                user_1 := GridUser(requested_net_import_kw=2),
                user_2 := GridUser(requested_net_import_kw=3),
            ],
        ),
        feeder_transformer_2 := Node(
            upper_limit=4,
            children=[
                user_3 := GridUser(requested_net_import_kw=2),
                user_4 := GridUser(requested_net_import_kw=1),
            ],
        ),
    ]
)
constrained_node_allocation_balancer(centralized_generation)
user_1.allocation  # 2.0
user_2.allocation  # 2.0
user_3.allocation  # 2.0
user_4.allocation  # 1.0
```

A notable difference between this and the fair internet bandwidth problem is that an internet user pays according to the maximum data transfer speed and maximum total data transfer available to them, while a grid user pays according to their *actual* 'data transfer speed' (power) and *actual* 'total data transfer' (energy). Beyond having implications to how the problems can be approached using the Constrained Node Allocation Balancer, this also just speaks to how much more reasonable the cost structure of the grid often is compared to internet service.
