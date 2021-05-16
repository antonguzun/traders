from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from tinvest import Candle


class StrategyParams:
    """
    n1 - кол-во дней перед днем с широким диапазоном, включенных в период PTR
    n2 - кол-во дней после дня с широким диапазоном, включенных в период PTR
    k - коэффициент волатильности - значение, которое должен превысить volatily ratio,
    чтобы определить день с широким диапазоном
    """
    n1 = 0
    n2 = 0
    k = 1.0


@dataclass
class PTR:
    """Price trigger range"""
    h: Decimal
    l: Decimal
    date: datetime

    @classmethod
    def create_by_candle(cls, candle: Candle) -> "PTR":
        return cls(candle.h, candle.l, candle.time)
