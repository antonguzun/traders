from dataclasses import dataclass
from datetime import date as date_type
from decimal import Decimal
from enum import Enum


class Direction(Enum):
    HIGH = "high"
    LOW = "low"


@dataclass
class RunDayBreakoutParams:
    """
    n1 - используется для определения дней ускорения. При n1 = 3 день будет определен,
    как день с верхним ускорением, если его истинный максимум выше,
    чем наибольший истинный максимум трех предыдущих дней, и его истинный минимум ниже,
    чем наименьший истинный минимум следующих трех дней;
    n2 - количество предшествующих дней с нижним ускорением, используемое для
    вычисления наибольшего истинного максимума, который должен быть превышен при закрытии,
    чтобы возник сигнал к покупке. (Кроме того, это количество предыдущих дней с верхним
    ускорением, используемое для вычисления наименьшего истинного минимума, который должен
    быть пробит ценой закрытия для формирования сигнала к продаже).
    """

    n1: int
    n2: int


@dataclass
class RunDay:
    """День ускорения - день с явно выраженным трендом
    день верхнего ускорения -
    день нижнего ускорения -
    """

    truth_max: Decimal
    truth_min: Decimal
    direction: Direction
    date: date_type

    @property
    def is_high(self) -> bool:
        return self.direction == Direction.HIGH

    @property
    def is_low(self) -> bool:
        return self.direction == Direction.LOW
