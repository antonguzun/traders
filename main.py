import datetime

from tinvest import SyncClient, CandleResolution

from bots.wide_ranging_day_bot.models import StrategyParams
from sim import Baffett, OnePaperHistoryWideRangeTrader
from sim.models import DealsView
from app.settings import TINKOFF_SANDBOX_TOKEN
from app.common.models.candle import Candle


def run_wide_range(ticker: str):
    client = SyncClient(TINKOFF_SANDBOX_TOKEN, use_sandbox=True)
    instrument_figi = client.get_market_search_by_ticker(ticker).payload.instruments[0].figi
    res = CandleResolution.day
    _from = datetime.datetime(year=2020, month=5, day=10)
    _to = datetime.datetime(year=2021, month=5, day=10)
    tinkoff_candles = client.get_market_candles(instrument_figi, _from, _to, res).payload.candles
    candles = [Candle.create_by_tinkoff_candle(t_candle) for t_candle in tinkoff_candles]
    print(f"TICKER {ticker}")
    print(f"date range: from {candles[0].time.date()} to {candles[-1].time.date()}")
    trader = OnePaperHistoryWideRangeTrader(StrategyParams(1, 2.3), is_short_on=True)
    active_deals = trader.create_deals(candles)
    passive_deals = Baffett().create_deals(candles)
    print("active deals:")
    [print(deal) for deal in active_deals]

    active_deals_view = DealsView(active_deals, candles[0].close)
    passive_deals_view = DealsView(passive_deals, candles[0].close)
    print(f"profit active {active_deals_view}")
    print(f"profit passive {passive_deals_view}")
    effect = round(active_deals_view.total_result_in_proc - passive_deals_view.total_result_in_proc, 2)
    print(f"profit effect {effect}%")


if __name__ == "__main__":
    tickers = ["SPCE",]
    for ticker in tickers:
        run_wide_range(ticker)
        print("________________________")
