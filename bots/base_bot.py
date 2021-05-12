from abc import ABC
from enum import Enum
from typing import List

from tinvest import Candle


class Decision(Enum):
    BUY = "buy"
    SELL = "sell"
    PASS = "pass"


class BaseBot(ABC):
    """ Базовый интерфейс бота
    При инициализации бота мы загоняем в него имеющиеся исторические данные
    При запуске метода __call__ передаем текущий candle, который в себе содержит цену акции и дату
    этот candle добавляется к историческим данным, и принимает решение "покупать/продавать" для последней даты
    """
    def __init__(self, history_candles: List[Candle]):
        self.history_candles = history_candles

    def __call__(self, candle: Candle) -> Decision:
        raise NotImplementedError
