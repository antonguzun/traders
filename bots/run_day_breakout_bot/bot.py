from decimal import Decimal
from typing import List, Optional

from app.common.actions.calculations import truth_max_of_candles, truth_min_of_candles
from app.common.models.candle import Candle
from bots.base_bot import BaseBot, Decision
from bots.run_day_breakout_bot.models import Direction, RunDay, RunDayBreakoutParams


class NotEnoughDataException(Exception):
    pass


class RunDayBreakoutBot(BaseBot):
    """Система пробоя дней ускорения (Run Days)

    Использование:
    После инициализации можно вызывать метод __сall__ и передать свежий candle,
    функция вернет решение по новому торговому дню типа Decision.
    """

    params: RunDayBreakoutParams

    def gen_new_run_day(self, candles: List[Candle]) -> Optional[RunDay]:
        prev_candles = candles[: self.params.n1]
        prev_candle = candles[self.params.n1 - 1]
        current_candle = candles[self.params.n1]
        post_candles = candles[self.params.n1 + 1 :]
        truth_max = max(current_candle.high, prev_candle.close)
        truth_min = min(current_candle.low, prev_candle.close)
        if truth_max > truth_max_of_candles(
            prev_candles
        ) and truth_min < truth_min_of_candles(post_candles):
            direction = Direction.HIGH
        elif truth_min < truth_min_of_candles(
            prev_candles
        ) and truth_max > truth_max_of_candles(post_candles):
            direction = Direction.LOW
        else:
            return None
        return RunDay(truth_max, truth_min, direction, candles[0].time.date())

    @property
    def run_days(self) -> List[RunDay]:
        candles = self.history_candles.copy()
        days = []
        for i in range(self.params.n1 + self.params.n2, len(candles)):
            day = self.gen_new_run_day(
                candles[i - self.params.n1 - self.params.n2 : i + 1]
            )
            if day:
                days.append(day)
        return days

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
