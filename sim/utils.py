from typing import List

from tinvest import Candle

from sim.models import Deal


def calc_passive_profit(candles: List[Candle]) -> List[Deal]:
    buy = Deal(candles[0].figi, candles[0].c, 1, candles[0].time)
    sell = Deal(candles[-1].figi, candles[-1].c, -1, candles[-1].time)
    return [buy, sell]
