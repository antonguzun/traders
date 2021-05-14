import datetime

from tinvest import SyncClient, CandleResolution

from sim.models import DealsView
from sim.sim_wide_ranging_day_bot import OnePaperHistoryWideRangeTrader
from sim.utils import calc_passive_profit
from app.settings import TINKOFF_SANDBOX_TOKEN


def run_wide_range(ticker: str):
    client = SyncClient(TINKOFF_SANDBOX_TOKEN, use_sandbox=True)
    instrument_figi = client.get_market_search_by_ticker(ticker).payload.instruments[0].figi

    res = CandleResolution.day
    _from = datetime.datetime(year=2020, month=5, day=10)
    _to = datetime.datetime(year=2021, month=5, day=10)
    c = client.get_market_candles(instrument_figi, _from, _to, res)
    print(f"TICKER {ticker}")
    print(f"date range: from {_from} to {_to}")
    trader = OnePaperHistoryWideRangeTrader(is_short_on=True)
    active_deals = trader.calc_active_profit(c.payload.candles)
    passive_deals = calc_passive_profit(c.payload.candles)

    active_deals_view = DealsView(active_deals, c.payload.candles[0].c)
    passive_deals_view = DealsView(passive_deals, c.payload.candles[0].c)

    print(f"profit active {active_deals_view}")
    print(f"profit passive {passive_deals_view}")
    effect = round(active_deals_view.total_result_in_proc - passive_deals_view.total_result_in_proc, 2)
    print(f"profit effect {effect}%")


if __name__ == "__main__":
    tickers = ["ACAD", "SPCE", "TSLA"]
    for ticker in tickers:
        run_wide_range(ticker)
        print("________________________")
