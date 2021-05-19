from decimal import Decimal
from typing import Optional, List

from app.common.models.candle import Candle

from bots.wide_ranging_day_bot.models import PTR, StrategyParams


class WideRangeDayGetter:
    def __init__(self, params: StrategyParams, candles: List[Candle]):
        self.params = params
        self.candles = candles

    @property
    def average_day_interval_for_required_days(self) -> Decimal:
        """интервал основывается на истинных(!) максимумах и минимумах"""
        last_interval = [abs(candle.open - candle.close) for candle in self.candles]
        return sum(last_interval) / len(self.candles)

    @property
    def last_day_interval(self) -> Decimal:
        """интервал основывается на истинных(!) максимумах и минимумах"""
        candle = self.candles[-1]
        return abs(candle.open - candle.close)

    @property
    def volatility_ratio(self) -> Decimal:
        return self.last_day_interval / self.average_day_interval_for_required_days

    @property
    def is_wide_range(self) -> bool:
        return self.volatility_ratio > self.params.k

    def __call__(self) -> Optional[Candle]:
        """Возвращает день с самым широким диапазоном из последних 1 + self.params.n1 дней
        при n1 = 0 эквивалентно
        if self.is_wide_range:
           return self.candles[-1]
        """
        widest_candle = None
        his_range = None

        for _ in range(self.params.n1):
            if self.is_wide_range and (not his_range or (his_range and self.volatility_ratio > his_range)):
                his_range = self.volatility_ratio
                widest_candle = self.candles.pop()
        return widest_candle


class PTRFinder:
    def __init__(self, params: StrategyParams, required_days_count: int, history_candles: List[Candle]):
        self.params = params
        self.required_days_count = required_days_count
        self.history_candles = history_candles

    @property
    def _candles(self) -> List[Candle]:
        """Возвращаем последний чанк дней длинной required_days_count"""
        return self.history_candles[-self.required_days_count:]

    @property
    def _last_candle(self) -> Candle:
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
    def _fresh_ptr(self) -> Optional[PTR]:
        """Если день является широкодиапазонным то возвращаем PTR на основе этого дня"""
        candles = self._candles
        day_with_wide_range = WideRangeDayGetter(self.params, candles.copy())()
        if day_with_wide_range:
            return PTR.create_by_candle(day_with_wide_range)
        return None

    def __call__(self, previous_ptr: Optional[PTR]) -> Optional[PTR]:
        """Либо находим актуальный PTR,
        либо возвращаем предыдущий,
        либо копаем историю
        """
        return self._fresh_ptr or previous_ptr or self._dig_ptr_from_history()
