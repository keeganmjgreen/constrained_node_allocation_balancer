Allocated min(ancestral_budgets) = 6.0 to leaf 1.1

```mermaid
flowchart TD
    1["<b>1</b><br>6.000 / 15.000<br><code>|████.....|</code>"]
    1.1["<b>1.1</b><br>6.000 / 6.000<br><code>|████|.....</code>"]
    1.2["<b>1.2</b><br>0.000 / 1.000<br><code>||.........</code>"]
    1.3["<b>1.3</b><br>0.000 / 9.000<br><code>|......|...</code>"]
    1 --> 1.1
    1 --> 1.2
    1 --> 1.3
```

Allocated min(ancestral_budgets) = 1.0 to leaf 1.2

```mermaid
flowchart TD
    1["<b>1</b><br>7.000 / 15.000<br><code>|████▋....|</code>"]
    1.1["<b>1.1</b><br>6.000 / 6.000<br><code>|████|.....</code>"]
    1.2["<b>1.2</b><br>1.000 / 1.000<br><code>||.........</code>"]
    1.3["<b>1.3</b><br>0.000 / 9.000<br><code>|......|...</code>"]
    1 --> 1.1
    1 --> 1.2
    1 --> 1.3
```

Allocated min(ancestral_budgets) = 8.0 to leaf 1.3

```mermaid
flowchart TD
    1["<b>1</b><br>15.000 / 15.000<br><code>|█████████|</code>"]
    1.1["<b>1.1</b><br>6.000 / 6.000<br><code>|████|.....</code>"]
    1.2["<b>1.2</b><br>1.000 / 1.000<br><code>||.........</code>"]
    1.3["<b>1.3</b><br>8.000 / 9.000<br><code>|█████▍|...</code>"]
    1 --> 1.1
    1 --> 1.2
    1 --> 1.3
```

Cleared allocations from all non-root nodes

```mermaid
flowchart TD
    1["<b>1</b><br>15.000 / 15.000<br><code>|█████████|</code>"]
    1.1["<b>1.1</b><br>0.000 / 6.000<br><code>|....|.....</code>"]
    1.2["<b>1.2</b><br>0.000 / 1.000<br><code>||.........</code>"]
    1.3["<b>1.3</b><br>0.000 / 9.000<br><code>|......|...</code>"]
    1 --> 1.1
    1 --> 1.2
    1 --> 1.3
```

Distributed 15.0 from node 1 to children ['1.1', '1.2', '1.3']

```mermaid
flowchart TD
    1["<b>1</b><br>15.000 / 15.000<br><code>|█████████|</code>"]
    1.1["<b>1.1</b><br>5.000 / 6.000<br><code>|███▍|.....</code>"]
    1.2["<b>1.2</b><br>5.000 / 1.000<br><code>||██▍......</code>"]
    1.3["<b>1.3</b><br>5.000 / 9.000<br><code>|███▍..|...</code>"]
    1 --> 1.1
    1 --> 1.2
    1 --> 1.3
```

Redistributed 4.0 from node 1.2 to siblings with headroom ['1.1', '1.3']

```mermaid
flowchart TD
    1["<b>1</b><br>15.000 / 15.000<br><code>|█████████|</code>"]
    1.1["<b>1.1</b><br>7.000 / 6.000<br><code>|████|.....</code>"]
    1.2["<b>1.2</b><br>1.000 / 1.000<br><code>||.........</code>"]
    1.3["<b>1.3</b><br>7.000 / 9.000<br><code>|████▋.|...</code>"]
    1 --> 1.1
    1 --> 1.2
    1 --> 1.3
```

Redistributed 1.0 from node 1.1 to siblings with headroom ['1.3']

```mermaid
flowchart TD
    1["<b>1</b><br>15.000 / 15.000<br><code>|█████████|</code>"]
    1.1["<b>1.1</b><br>6.000 / 6.000<br><code>|████|.....</code>"]
    1.2["<b>1.2</b><br>1.000 / 1.000<br><code>||.........</code>"]
    1.3["<b>1.3</b><br>8.000 / 9.000<br><code>|█████▍|...</code>"]
    1 --> 1.1
    1 --> 1.2
    1 --> 1.3
```

