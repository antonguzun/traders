from datetime import datetime
from typing import List

from tinvest import CandleResolution, SyncClient

from app.common.models.candle import Candle


class TIClient(SyncClient):
    def get_candles(self, ticker: str, _from: datetime, _to: datetime) -> List[Candle]:
        instrument_figi = (
            self.get_market_search_by_ticker(ticker).payload.instruments[0].figi
        )
        res = CandleResolution.day
        tinkoff_candles = self.get_market_candles(
            instrument_figi, _from, _to, res
        ).payload.candles
        return [
            Candle.create_by_tinkoff_candle(t_candle) for t_candle in tinkoff_candles
        ]