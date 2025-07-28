from typing import Self

from pydantic import BaseModel, model_validator


class Range(BaseModel):
    lower: float = 0.0
    upper: float = float("inf")

    @model_validator(mode="after")
    def validate(self) -> Self:
        if self.lower > self.upper:
            raise ValueError("lower must be <= upper")
        return self

    def contains(self, value: float, inclusive: bool = True) -> bool:
        if inclusive:
            return self.lower <= value <= self.upper
        else:
            return self.lower < value < self.upper

    def excess(self, value: float) -> float:
        if value < self.lower:
            return self.lower - value
        elif value > self.upper:
            return value - self.upper
        else:
            return 0.0
