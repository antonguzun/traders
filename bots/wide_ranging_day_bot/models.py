from dataclasses import dataclass
from decimal import Decimal

from tinvest import Candle


class StrategyParams:
    n1 = 0
    n2 = 0
    k = 1.7


@dataclass
class PTR:
    h: Decimal
    l: Decimal

    @classmethod
    def create_by_candle(cls, candle: Candle) -> "PTR":
        return cls(candle.h, candle.l)
