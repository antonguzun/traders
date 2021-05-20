from decimal import Decimal
from typing import List, Optional

from app.common.models.candle import Candle
from bots.base_bot import BaseBot, Decision
from bots.run_day_breakout_bot.actions import RunDayCreator
from bots.run_day_breakout_bot.models import RunDay, RunDayBreakoutParams


class NotEnoughDataException(Exception):
    pass


class RunDayBreakoutBot(BaseBot):
    """Система пробоя дней ускорения (Run Days)

    Использование:
    После инициализации можно вызывать метод __сall__ и передать свежий candle,
    функция вернет решение по новому торговому дню типа Decision.
    """

    params: RunDayBreakoutParams

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_days = RunDayCreator(
            days_before_count=self.params.n1, follow_days_count=self.params.n1
        )

    @property
    def run_days(self) -> List[RunDay]:
        return self.get_days(self.history_candles)

    @property
    def last_run_day(self) -> Optional[RunDay]:
        return self.run_days[-1]

    @property
    def low_run_days(self) -> List[RunDay]:
        days = []
        for day in self.run_days:
            if day.is_low:
                days.append(day)
        return days

    @property
    def high_run_days(self) -> List[RunDay]:
        days = []
        for day in self.run_days:
            if day.is_high:
                days.append(day)
        return days

    @property
    def max_of_low_run_days(self) -> Decimal:
        low_run_days = self.low_run_days[-self.params.n2 :]
        max_values = [run_day.truth_max for run_day in low_run_days]
        try:
            return max(max_values)
        except ValueError:
            raise NotEnoughDataException

    @property
    def min_of_high_run_days(self) -> Decimal:
        high_run_days = self.high_run_days[-self.params.n2 :]
        min_values = [run_day.truth_min for run_day in high_run_days]
        try:
            return min(min_values)
        except ValueError:
            raise NotEnoughDataException

    def __call__(self, candle: Candle) -> Decision:
        self.history_candles.append(candle)
        try:
            if candle.close > self.max_of_low_run_days and self.last_run_day.is_high:
                return Decision.BUY
            elif candle.close < self.min_of_high_run_days and self.last_run_day.is_low:
                return Decision.SELL
        except NotEnoughDataException:
            pass
        return Decision.PASS
