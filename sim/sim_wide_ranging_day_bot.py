from bots.wide_ranging_day_bot.bot import WideRangeDayBot
from sim.base.traders import OnePaperHistoryBaseTrader


class OnePaperHistoryWideRangeTrader(OnePaperHistoryBaseTrader):
    bot_class = WideRangeDayBot
