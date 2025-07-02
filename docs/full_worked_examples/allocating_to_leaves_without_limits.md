Allocated min(ancestral_budgets) = 2.0 to leaf 1.1

```mermaid
flowchart TD
    1["<b>1</b><br>2.000 / 2.000<br><code>|█████████|</code>"]
    1.1["<b>1.1</b><br>2.000<br><code>|██████████</code>"]
    1.2["<b>1.2</b><br>0.000<br><code>|..........</code>"]
    1 --> 1.1
    1 --> 1.2
```

Allocated min(ancestral_budgets) = 0.0 to leaf 1.2

```mermaid
flowchart TD
    1["<b>1</b><br>2.000 / 2.000<br><code>|█████████|</code>"]
    1.1["<b>1.1</b><br>2.000<br><code>|██████████</code>"]
    1.2["<b>1.2</b><br>0.000<br><code>|..........</code>"]
    1 --> 1.1
    1 --> 1.2
```

Cleared allocations from all non-root nodes

```mermaid
flowchart TD
    1["<b>1</b><br>2.000 / 2.000<br><code>|█████████|</code>"]
    1.1["<b>1.1</b><br>0.000<br><code>|..........</code>"]
    1.2["<b>1.2</b><br>0.000<br><code>|..........</code>"]
    1 --> 1.1
    1 --> 1.2
```

Distributed 2.0 from node 1 to children ['1.1', '1.2']

```mermaid
flowchart TD
    1["<b>1</b><br>2.000 / 2.000<br><code>|█████████|</code>"]
    1.1["<b>1.1</b><br>1.000<br><code>|█████.....</code>"]
    1.2["<b>1.2</b><br>1.000<br><code>|█████.....</code>"]
    1 --> 1.1
    1 --> 1.2
```

