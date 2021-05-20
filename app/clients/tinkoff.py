from datetime import datetime
from typing import List

from tinvest import CandleResolution, SyncClient

from app.clients.base import BaseClient
from app.common.models.candle import Candle


class TIClient(BaseClient, SyncClient):
    def get_candles_by_ticker(
        self, ticker: str, _from: datetime, _to: datetime
    ) -> List[Candle]:
        instrument_figi = (
            self.get_market_search_by_ticker(ticker).payload.instruments[0].figi
        )
        tinkoff_candles = self.get_market_candles(
            instrument_figi, _from, _to, CandleResolution.day
        ).payload.candles
        return [
            Candle.create_by_tinkoff_candle(t_candle) for t_candle in tinkoff_candles
        ]
