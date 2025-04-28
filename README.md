# Constrained Node Allocation Balancer

The constrained node allocation balancer is an algorithm designed for tree data structures in which:

- Each leaf node is given an allotment (some value or amount).
- Each parent node's allotment is equal to the sum of its child nodes' allotments.
- Nodes are constrained by a limit on their maximum allotment.

The algorithm distributes, or balances, the allotments among the leaf nodes as evenly as possible given the aforementioned constraint.

## Getting started

Assuming you are using a Linux-based OS:

1. Install Poetry: `curl https://install.python-poetry.org | python3`
2. `poetry config virtualenvs.in-project false`
3. Create the project's virtual environment (based on `pyproject.toml`): `poetry install`

Assuming you are using VS Code:

4. Add `"python.venvPath": "~/.cache/pypoetry/virtualenvs/"` to your **user** `settings.json`.
5. Select `constrained-node-allocation-balancer-<hash>-<python-version>` as your Python interpreter.

## Algorithm

### Step 1: Determine the root allotment

*Function `set_root_allotment`.*

The algorithm's first step is determining the allotment of the tree's root node. This is equal to the largest possible sum of the tree's leaf allotments. The algorithm determines this by iterating over the leaves, in any order, and allocating the largest possible allotment to each leaf that satisfies that leaf's limit (if any) and the limits of its ancestors. Each node has a 'remaining budget'; in the beginning, a node's budget is set to its limit. As an allotment is allocated to a leaf (and thus to its ancestors), that leaf's budget is reduced by the same amount (along with the budgets of its ancestors). So, each leaf is assigned the minimum of the budget of the leaf and of its ancestors. At the end of iterating over the leaves, the allotment of the root node will be equal to the largest possible sum of the leaf allotments.

Theorem: The root allotment will be the same regardless of the order in which the leaves are iterated over, even if the leaf allotments would in general be different. In other words, every `Node.children: list[Node]` can be reordered arbitrarily without consequence.

### Step 2: Remove inactive constraints

*Function `remove_inactive_constraints`.*

The tree may have nodes whose limits can never be reached due to the limits of those nodes's children. Such nodes will be referred to as inactive nodes because they represent inactive constraints; they do not end up limiting their own allotment or that of their children. Inactive nodes TODO

The algorithm's second step is removing the limits from any inactive nodes.

### Step 3: Balance the descendent nodes' allotments

*Function `constrained_node_allocation_balancer`.*

The algorithm's third and main step is to traverse the tree and distribute the root allotment as evenly as possible at each level (starting with the root's children, ending with the deepest leaves) subject to the nodes' limits.

Definition: A node's *level* is its distance from the root node, with the root being the only level 0 node and the deepest leaves having the greatest level.

The tree is traversed from root to leaves because...

The tree is traversed level by level (iterating over the nodes at each level) because...

Theorem: When distributing the root allotment level by level, root to leaves, it is impossible for a node X to receive an allotment that is too much for its descendants. Say the leaves among those descendents were the first to be iterated over and thus recieved the largest possible allotment satisfying their and their parents' limits. If node X's limit was reached, then node X's descendants are guaranteed to have headroom. If node X's limit was not reached,
Remove inactive

Limiting children???
- theorem
