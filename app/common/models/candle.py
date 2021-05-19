from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Candle:
    name: str
    open: Decimal
    close: Decimal
    high: Decimal
    low: Decimal
    time: datetime

    @classmethod
    def create_by_tinkoff_candle(cls, t_candle) -> "Candle":
        return cls(t_candle.figi, t_candle.o, t_candle.c, t_candle.h, t_candle.l, t_candle.time)
