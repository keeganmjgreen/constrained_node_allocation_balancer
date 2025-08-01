Allocated min(ancestral_budgets) = 10.0 to leaf 1.1.1

```mermaid
flowchart TD
    1["<b>1</b><br>10.000<br><code>|█.........</code>"]
    1.1["<b>1.1</b><br>10.000 / 20.000<br><code>|█.|.......</code>"]
    1.1.1["<b>1.1.1</b><br>10.000 / 10.000<br><code>|█|........</code>"]
    1.2["<b>1.2</b><br>0.000 / 80.000<br><code>|........|.</code>"]
    1.2.1["<b>1.2.1</b><br>0.000 / 100.000<br><code>|.........|</code>"]
    1 --> 1.1
    1.1 --> 1.1.1
    1 --> 1.2
    1.2 --> 1.2.1
```

Allocated min(ancestral_budgets) = 80.0 to leaf 1.2.1

```mermaid
flowchart TD
    1["<b>1</b><br>90.000<br><code>|█████████.</code>"]
    1.1["<b>1.1</b><br>10.000 / 20.000<br><code>|█.|.......</code>"]
    1.1.1["<b>1.1.1</b><br>10.000 / 10.000<br><code>|█|........</code>"]
    1.2["<b>1.2</b><br>80.000 / 80.000<br><code>|████████|.</code>"]
    1.2.1["<b>1.2.1</b><br>80.000 / 100.000<br><code>|████████.|</code>"]
    1 --> 1.1
    1.1 --> 1.1.1
    1 --> 1.2
    1.2 --> 1.2.1
```

Cleared allocations from all non-root nodes

```mermaid
flowchart TD
    1["<b>1</b><br>90.000<br><code>|█████████.</code>"]
    1.1["<b>1.1</b><br>0.000 / 20.000<br><code>|..|.......</code>"]
    1.1.1["<b>1.1.1</b><br>0.000 / 10.000<br><code>|.|........</code>"]
    1.2["<b>1.2</b><br>0.000 / 80.000<br><code>|........|.</code>"]
    1.2.1["<b>1.2.1</b><br>0.000 / 100.000<br><code>|.........|</code>"]
    1 --> 1.1
    1.1 --> 1.1.1
    1 --> 1.2
    1.2 --> 1.2.1
```

Set limit of node 1.1 to the sum of its children's limits 10

```mermaid
flowchart TD
    1["<b>1</b><br>90.000<br><code>|█████████.</code>"]
    1.1["<b>1.1</b><br>0.000 / 10.000<br><code>|.|........</code>"]
    1.1.1["<b>1.1.1</b><br>0.000 / 10.000<br><code>|.|........</code>"]
    1.2["<b>1.2</b><br>0.000 / 80.000<br><code>|........|.</code>"]
    1.2.1["<b>1.2.1</b><br>0.000 / 100.000<br><code>|.........|</code>"]
    1 --> 1.1
    1.1 --> 1.1.1
    1 --> 1.2
    1.2 --> 1.2.1
```

Distributed 90.0 from node 1 to children ['1.1', '1.2']

```mermaid
flowchart TD
    1["<b>1</b><br>90.000<br><code>|█████████.</code>"]
    1.1["<b>1.1</b><br>45.000 / 10.000<br><code>|█|██▌.....</code>"]
    1.1.1["<b>1.1.1</b><br>0.000 / 10.000<br><code>|.|........</code>"]
    1.2["<b>1.2</b><br>45.000 / 80.000<br><code>|████▌...|.</code>"]
    1.2.1["<b>1.2.1</b><br>0.000 / 100.000<br><code>|.........|</code>"]
    1 --> 1.1
    1.1 --> 1.1.1
    1 --> 1.2
    1.2 --> 1.2.1
```

Redistributed 35.0 from node 1.1 to siblings with headroom ['1.2']

```mermaid
flowchart TD
    1["<b>1</b><br>90.000<br><code>|█████████.</code>"]
    1.1["<b>1.1</b><br>10.000 / 10.000<br><code>|█|........</code>"]
    1.1.1["<b>1.1.1</b><br>0.000 / 10.000<br><code>|.|........</code>"]
    1.2["<b>1.2</b><br>80.000 / 80.000<br><code>|████████|.</code>"]
    1.2.1["<b>1.2.1</b><br>0.000 / 100.000<br><code>|.........|</code>"]
    1 --> 1.1
    1.1 --> 1.1.1
    1 --> 1.2
    1.2 --> 1.2.1
```

Distributed 10.0 from node 1.1 to children ['1.1.1']

```mermaid
flowchart TD
    1["<b>1</b><br>90.000<br><code>|█████████.</code>"]
    1.1["<b>1.1</b><br>10.000 / 10.000<br><code>|█|........</code>"]
    1.1.1["<b>1.1.1</b><br>10.000 / 10.000<br><code>|█|........</code>"]
    1.2["<b>1.2</b><br>80.000 / 80.000<br><code>|████████|.</code>"]
    1.2.1["<b>1.2.1</b><br>0.000 / 100.000<br><code>|.........|</code>"]
    1 --> 1.1
    1.1 --> 1.1.1
    1 --> 1.2
    1.2 --> 1.2.1
```

Distributed 80.0 from node 1.2 to children ['1.2.1']

```mermaid
flowchart TD
    1["<b>1</b><br>90.000<br><code>|█████████.</code>"]
    1.1["<b>1.1</b><br>10.000 / 10.000<br><code>|█|........</code>"]
    1.1.1["<b>1.1.1</b><br>10.000 / 10.000<br><code>|█|........</code>"]
    1.2["<b>1.2</b><br>80.000 / 80.000<br><code>|████████|.</code>"]
    1.2.1["<b>1.2.1</b><br>80.000 / 100.000<br><code>|████████.|</code>"]
    1 --> 1.1
    1.1 --> 1.1.1
    1 --> 1.2
    1.2 --> 1.2.1
```

