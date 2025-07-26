import math
from copy import deepcopy
from pathlib import Path
from typing import Literal

from node import Node


class Logs:
    _tree_snapshots: dict[str, Node]

    def __init__(self) -> None:
        self._tree_snapshots = {}

    def add(self, message: str, tree: Node) -> None:
        self._tree_snapshots[message] = deepcopy(tree)

    def show(self, how: Literal["ascii", "mermaid"] = "ascii") -> None:
        for message, tree in self._tree_snapshots.items():
            print(message)
            tree.show(
                max_allocation_str_len=self._max_allocation_str_len,
                max_limit_str_len=self._max_limit_str_len,
                max_value=self._max_value,
                how=how,
            )

    def write(
        self, file: Path | str, how: Literal["ascii", "mermaid"] = "ascii"
    ) -> None:
        file = Path(file)
        with file.open(mode="w") as f:
            for message, tree in self._tree_snapshots.items():
                f.write(message + "\n")
                f.write("\n")
                f.write(f"```{'mermaid' if how == 'mermaid' else ''}\n")
                f.write(
                    tree.tree_repr(
                        max_allocation_str_len=self._max_allocation_str_len,
                        max_limit_str_len=self._max_limit_str_len,
                        max_value=self._max_value,
                        how=how,
                    )
                )
                f.write("\n")
                f.write("```\n")
                f.write("\n")

    @property
    def _max_value(self) -> float:
        return max(self._max_allocation, self._max_limit)

    @property
    def _max_allocation_str_len(self) -> int:
        return len(f"{self._max_allocation:.3f}")

    @property
    def _max_limit_str_len(self) -> int:
        return len(f"{self._max_limit:.3f}")

    @property
    def _max_allocation(self) -> float:
        return max(
            n.allocation
            for tree in self._tree_snapshots.values()
            for n in tree.all_nodes
        )

    @property
    def _max_limit(self) -> float:
        return max(
            n.limit
            for tree in self._tree_snapshots.values()
            for n in tree.all_nodes
            if not math.isinf(n.limit)
        )
