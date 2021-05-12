from decimal import Decimal
from typing import Optional, List

from tinvest import Candle

from bots.wide_ranging_day_bot.models import PTR, StrategyParams


class LastDayIsWideRange:
    def __init__(self, params: StrategyParams, candles: List[Candle]):
        self.params = params
        self.candles = candles

    @property
    def average_day_interval_for_required_days(self) -> Decimal:
        last_interval = [abs(candle.h - candle.l) for candle in self.candles]
        return sum(last_interval) / len(self.candles)

    @property
    def last_day_interval(self) -> Decimal:
        candle = self.candles[-1]
        return abs(candle.h - candle.l)

    @property
    def volatility_ratio(self) -> Decimal:
        return self.last_day_interval / self.average_day_interval_for_required_days

    def __call__(self) -> bool:
        return self.volatility_ratio > self.params.k


class PTRFinder:
    def __init__(self, params: StrategyParams, required_days_count: int, history_candles: List[Candle]):
        self.params = params
        self.required_days_count = required_days_count
        self.history_candles = history_candles

    @property
    def _candles(self):
        """Возвращаем последний чанк дней длинной required_days_count"""
        return self.history_candles[-self.required_days_count:]

    @property
    def _last_candle(self):
        return self.history_candles[-1]

    def _dig_ptr_from_history(self) -> Optional[PTR]:
        """Копаем путем удаления дней с конца и высчитываем "свежий" PTR с учетом удаленного дня"""
        while len(self.history_candles) >= self.required_days_count:
            self.history_candles.pop()
            ptr = self._fresh_ptr
            if ptr:
                return ptr
        return None

    @property
    def _fresh_ptr(self):
        """Если день является широкодиапазонным то возвращаем PTR на основе этого дня"""
        candles = self._candles
        check_day_is_wide_range = LastDayIsWideRange(self.params, candles)
        if check_day_is_wide_range():
            return PTR.create_by_candle(self._last_candle)
        return None

    def __call__(self, previous_ptr: Optional[PTR]) -> Optional[PTR]:
        """Либо находим актуальный PTR,
        либо возвращаем предыдущий,
        либо копаем историю
        """
        return self._fresh_ptr or previous_ptr or self._dig_ptr_from_history()
