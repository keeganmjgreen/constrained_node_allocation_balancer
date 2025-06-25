# The Algorithm

The Constrained Node Allocation Balancer algorithm can be broken down into three steps:

- Determining the root allocation.
- Adjusting inactive limits.
- Balancing the descendant nodes' allocations.

Each of these steps corresponds to an internal function called by `constrained_node_allocation_balancer`.


## Step 1: Determining the root allocation

*Function `_set_root_allocation`.*

The algorithm's first step is determining the allocation of the tree's root node. This is equal to the largest possible sum of the tree's leaf allocations. The algorithm determines this by iterating over the leaves, in any order, and allocating the largest possible allocation to each leaf that satisfies that leaf's limit (if any) and the limits of its ancestors. Each node has a 'remaining budget'; in the beginning, a node's budget is set to its limit. As an allocation is allocated to a leaf (and thus to its ancestors), that leaf's budget is reduced by the same amount (along with the budgets of its ancestors). So, each leaf is assigned the minimum of the budget of the leaf and of its ancestors. At the end of iterating over the leaves, the allocation of the root node will be equal to the largest possible sum of the leaf allocations.

!!! Theorem
    The root allocation will be the same regardless of the order in which the leaves are iterated over, even if the leaf allocations would in general be different. In other words, every `Node.children: list[Node]` can be reordered arbitrarily without consequence.


## Step 2: Adjusting inactive limits

*Function `_adjust_inactive_limits`.*

The tree may have nodes without limits or nodes whose limits can never be reached due to the limits of those nodes's children. Such nodes will be referred to as inactive nodes because they represent inactive limits; they do not end up limiting their own allocation or that of their children. Inactive nodes TODO

The algorithm's second step is adjusting the limits of any inactive nodes.


## Step 3: Balancing the descendant nodes' allocations

*Function `_balance_allocations`.*

The algorithm's third and main step is to traverse the tree and distribute the root allocation as evenly as possible at each level (starting with the root's children, ending with the deepest leaves) subject to the nodes' limits.

!!! Definition
    A node's *level* is its distance from the root node, with the root being the only level 0 node and the deepest leaves having the greatest level.

The tree is traversed from root to leaves because...

The tree is traversed level by level (iterating over the nodes at each level) because...

!!! Theorem:
    When distributing the root allocation level by level, root to leaves, it is impossible for a node X to receive an allocation that is too much for its descendants. Say the leaves among those descendants were the first to be iterated over and thus recieved the largest possible allocation satisfying their and their parents' limits. If node X's limit was reached, then node X's descendants are guaranteed to have headroom. If node X's limit was not reached,
Remove inactive

Limiting children???
- theorem
