from typing import List, Optional

from app.common.actions.calculations import truth_max_of_candles, truth_min_of_candles
from app.common.models.candle import Candle
from bots.run_day_breakout_bot.models import Direction, RunDay


class RunDayCreator:
    """Класс содержит в себе логику по созданию и фильтрации дней с ускорением"""

    def __init__(self, days_before_count: int, follow_days_count: int):
        self.days_before_count = days_before_count
        self.follow_days_count = follow_days_count

    @staticmethod
    def is_high_run_day(truth_max, truth_min, candles_before, candles_follow) -> bool:
        return truth_max > truth_max_of_candles(
            candles_before
        ) and truth_min < truth_min_of_candles(candles_follow)

    @staticmethod
    def is_low_run_day(truth_max, truth_min, candles_before, candles_follow) -> bool:
        return truth_min < truth_min_of_candles(
            candles_before
        ) and truth_max > truth_max_of_candles(candles_follow)

    def get_run_day_by_candles(self, candles: List[Candle]) -> Optional[RunDay]:
        candles_before = candles[: self.days_before_count]
        candles_follow = candles[self.days_before_count + 1 :]
        prev_candle = candles[self.days_before_count - 1]
        current_candle = candles[self.days_before_count]
        truth_max = max(current_candle.high, prev_candle.close)
        truth_min = min(current_candle.low, prev_candle.close)
        if self.is_high_run_day(truth_max, truth_min, candles_before, candles_follow):
            direction = Direction.HIGH
        elif self.is_low_run_day(truth_max, truth_min, candles_before, candles_follow):
            direction = Direction.LOW
        else:
            return None
        return RunDay(truth_max, truth_min, direction, candles[0].time.date())

    def get_run_days(self, candles: List[Candle]) -> List[RunDay]:
        days = []
        required_candles_count = self.days_before_count + self.days_before_count
        for i in range(required_candles_count, len(candles)):
            candles_chunk = candles[i - required_candles_count : i + 1]
            day = self.get_run_day_by_candles(candles_chunk)
            if day:
                days.append(day)
        return days

    def __call__(self, candles: List[Candle]) -> List[RunDay]:
        return self.get_run_days(candles)
