from typing import List

from app.common.models.candle import Candle
from bots.run_day_breakout_bot.bot import RunDayBreakoutBot
from bots.run_day_breakout_bot.models import RunDayBreakoutParams
from bots.wide_ranging_day_bot.bot import WideRangeDayBot
from bots.wide_ranging_day_bot.models import WideRangeParams
from sim.base import BaseTrader, OnePaperHistoryBaseTrader
from sim.models import Deal


class Baffett(BaseTrader):
    def create_deals(self, candles: List[Candle]) -> List[Deal]:
        buy = Deal(candles[0].name, candles[0].close, 1, candles[0].time)
        sell = Deal(candles[-1].name, candles[-1].close, -1, candles[-1].time)
        return [buy, sell]


class OnePaperHistoryWideRangeTrader(OnePaperHistoryBaseTrader):
    bot_class = WideRangeDayBot
    params: WideRangeParams


class OnePaperHistoryRunDayBreakoutTrader(OnePaperHistoryBaseTrader):
    bot_class = RunDayBreakoutBot
    params: RunDayBreakoutParams
