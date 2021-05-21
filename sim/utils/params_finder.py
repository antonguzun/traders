from datetime import datetime

from bots.run_day_breakout_bot.models import RunDayBreakoutParams
from bots.wide_ranging_day_bot.models import WideRangeParams
from sim import OnePaperHistoryWideRangeTrader


def gen_params():
    for j in range(10, 25):
        for i in range(0, 7):
            yield WideRangeParams(i, j / 10)


def find_wide_range_params(candles) -> WideRangeParams:
    profit = 0
    best_params = None
    for params in gen_params():
        trader = OnePaperHistoryWideRangeTrader(params, is_short_on=True)
        local_profit = sum(trader.create_deals(candles))
        if local_profit > profit:
            profit = local_profit
            best_params = params
    return best_params


def find_days_breakout_params(_) -> RunDayBreakoutParams:
    # todo
    return RunDayBreakoutParams(3, 3)
