from app.common.models.candle import Candle
from bots.base_bot import BaseBot, Decision
from bots.wide_ranging_day_bot.actions import PTRFinder
from bots.wide_ranging_day_bot.models import WideRangeParams


class WideRangeDayBot(BaseBot):
    """Система широкодиапазонного дня, использует сущность PTR.

    Использование:
    После инициализации можно вызывать метод __сall__ и передать свежий candle,
    функция вернет решение по новому торговому дню типа Decision.
    """

    params: WideRangeParams
    required_days_count = 10
    ptr = None

    @property
    def can_make_decision(self) -> bool:
        """Если недостаточно данных - не можем принять решение"""
        return len(self.history_candles) >= self.required_days_count

    def __call__(self, candle: Candle) -> Decision:
        self.history_candles.append(candle)

        if not self.can_make_decision:
            return Decision.PASS

        find_ptr = PTRFinder(
            self.params, self.required_days_count, self.history_candles.copy()
        )
        self.ptr = find_ptr(self.ptr)

        if self.ptr:
            if candle.close > self.ptr.h:
                return Decision.BUY
            elif candle.close < self.ptr.l:
                return Decision.SELL
        return Decision.PASS
