# The Algorithm

The Constrained Node Allocation Balancer algorithm can be broken down into three steps:

- Determining the root allocation.
- Adjusting inactive limits.
- Balancing the descendant nodes' allocations.

Each of these steps corresponds to an internal function called by `constrained_node_allocation_balancer`.


## Step 1: Determining the root allocation

*Function `_set_root_allocation`.*

The algorithm's first step is determining the maximum possible allocation of the tree's root node. This is equal to the largest possible sum of allocations to the tree's leaves. The algorithm determines this by iterating over the leaves, in any order, and allocating the largest possible allocation to each leaf that satisfies that leaf's limit (if any) and the limits of its ancestors. Each node has a "remaining budget"; in the beginning, a node's budget is set to its limit. As an allocation is given to a leaf (and thus to its ancestors), that leaf's budget is reduced by that amount (along with the budgets of its ancestors). Thus, each leaf is assigned the minimum of the budget of the leaf and of its ancestors. After iterating over the leaves, the allocation of the root node will be equal to the largest possible sum of the leaf allocations.

!!! Theorem
    The root allocation will be the same regardless of the order in which the leaves are iterated over, even if the leaf allocations would in general be different. In other words, every `Node.children: list[Node]` can be reordered arbitrarily without consequence.


## Step 2: Adjusting inactive limits

*Function `_adjust_inactive_limits`.*

The tree may have nodes that do not have limits or whose limits can never be reached due to the limits of those nodes's children. Such nodes' limits will be referred to as inactive limits because they represent inactive constraints; their nodes do not end up limiting their own allocation or that of their children. Because the allocation of a parent affects the allocations to its children in Step 3, and depends on the parent's limit, the parent's limit must be set/adjusted to the sum of its children's limits (the children's "throughput"). Doing this throughout the tree is the algorithm's second step. This must be done starting from the level of the tree's deepest leaves and ending with the tree's root node, because the adjustment of a parent based on its children depends on the adjustment of each of the children based on their respective (grand)children; the dependencies are from leaves to root rather than from root to leaves.


## Step 3: Balancing the descendant nodes' allocations

*Function `_balance_allocations`.*

The algorithm's third and main step is to traverse the tree and distribute the root allocation as evenly as possible at each level (starting with the root's children, ending with the deepest leaves) subject to the nodes' limits.

!!! Definition
    A node's *level* is its distance from the root node, with the root being the only level 0 node and the deepest leaves having the greatest level.

The tree is traversed from root to leaves because the allocation to a child is based on its parent's allocation depends on the parent's allocation to its own (grand)parent. This direction of traversal is opposite to Step 2. The tree is traversed in level-order, iterating over the nodes at each level and balancing the allocation between them; this *breadth-first* traversal order is used instead of a *depth-first* order because the allocations to a parent's children depends not only on that parent, but also on that parent's siblings, among whom their own (grand)parent's allocation is balanced.
