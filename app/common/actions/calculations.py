from decimal import Decimal
from typing import List

from app.common.models.candle import Candle


def truth_max_of_candles(candles: List[Candle]) -> Decimal:
    max_values = []
    for i in range(len(candles)):
        if i == 0:
            max_values.append(candles[i].close)
        else:
            max_values.append(max(candles[i].high, candles[i - 1].close))
    return max(*max_values)


def truth_min_of_candles(candles: List[Candle]) -> Decimal:
    min_values = []
    for i in range(len(candles)):
        if i == 0:
            min_values.append(candles[i].close)
        else:
            min_values.append(min(candles[i].low, candles[i - 1].close))
    return min(*min_values)
