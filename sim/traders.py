from typing import List

from app.common.models.candle import Candle

from bots.wide_ranging_day_bot.bot import WideRangeDayBot
from bots.wide_ranging_day_bot.models import StrategyParams
from sim.models import Deal
from sim.base import OnePaperHistoryBaseTrader


class Baffett:
    @staticmethod
    def create_deals(candles: List[Candle]) -> List[Deal]:
        buy = Deal(candles[0].name, candles[0].close, 1, candles[0].time)
        sell = Deal(candles[-1].name, candles[-1].close, -1, candles[-1].time)
        return [buy, sell]


class OnePaperHistoryWideRangeTrader(OnePaperHistoryBaseTrader):
    bot_class = WideRangeDayBot
    params: StrategyParams
