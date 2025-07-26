<div align="center">
    <img src="docs/logo.svg" alt="Constrained Node Allocation Balancer" width=50% />
    <p><a href="https://keeganmjgreen.github.io/constrained_node_allocation_balancer/index.html"><b>Docs</b></a><p>
</div>

# Constrained Node Allocation Balancer

The Constrained Node Allocation Balancer is an algorithm designed for tree data structures in which:

- Each leaf node is to be given an allocation (some value or amount).
- Each parent node's allocation is equal to the sum of its child nodes' allocations.
- Nodes are optionally constrained by a limit on their maximum allocation.

Subject to the nodes' limits, the algorithm assigns the largest possible allocation to the tree overall, and distributes, or balances, the allocations among the leaf nodes as evenly as possible.

## Applications

This algorithm is useful in any application where some concept of fairness is constrained by tree or network-like limits. For example, giving internet or network users maximum possible bandwidth, subject to network constraints, without arbitrarily giving one user more bandwidth than another. Or, giving electricity consumers maximum possible power, subject to electricity grid constraints, without arbitrarily giving one consumer more power than another.
