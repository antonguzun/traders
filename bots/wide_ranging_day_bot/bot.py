from tinvest import Candle

from bots.base_bot import BaseBot, Decision
from bots.wide_ranging_day_bot.actions import PTRFinder
from bots.wide_ranging_day_bot.models import StrategyParams


class WideRangeDayBot(BaseBot):
    """Генерирует сигналы на действия с активом
    Основан на работе с сущностью PTR и принципе широкодиапазонного дня
    После инициализации можно вызывать метод __сall__ и получать решение по новому торговому дню
    """
    params = StrategyParams()
    required_days_count = 10
    ptr = None

    def check_initial_data(self):
        assert len(self.history_candles) >= self.required_days_count, "Недостаточная история"

    def __call__(self, candle: Candle) -> Decision:
        self.check_initial_data()
        self.history_candles.append(candle)

        find_ptr = PTRFinder(self.params, self.required_days_count, self.history_candles.copy())
        self.ptr = find_ptr(self.ptr)

        if self.ptr:
            if candle.c > self.ptr.h:
                return Decision.BUY
            elif candle.c < self.ptr.l:
                return Decision.SELL
        return Decision.PASS
