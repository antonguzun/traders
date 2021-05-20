from app.common.models.candle import Candle
from bots.base_bot import BaseBot, Decision
from bots.run_day_breakout_bot.models import DayBreakoutParams


class RunDayBreakoutBot(BaseBot):
    """Система пробоя дней ускорения

    Использование:
    После инициализации можно вызывать метод __сall__ и передать свежий candle,
    функция вернет решение по новому торговому дню типа Decision.
    """
    params: DayBreakoutParams

    def __call__(self, candle: Candle) -> Decision:
        return Decision.PASS
