from abc import ABC
from datetime import datetime
from typing import List

from app.common.models.candle import Candle


class BaseClient(ABC):
    def get_candles_by_ticker(
        self, ticker: str, _from: datetime, _to: datetime
    ) -> List[Candle]:
        raise NotImplementedError
