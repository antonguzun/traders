from datetime import datetime

from app.clients.tinkoff import TIClient
from bots.wide_ranging_day_bot.models import StrategyParams
from sim import Baffett, OnePaperHistoryWideRangeTrader
from sim.models import DealsView
from app.settings import TINKOFF_SANDBOX_TOKEN


def run_wide_range(ticker: str, _from: datetime, _to: datetime):
    client = TIClient(TINKOFF_SANDBOX_TOKEN, use_sandbox=True)
    candles = client.get_candles(ticker, _from, _to)

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
    _from = datetime(year=2020, month=5, day=10)
    _to = datetime(year=2021, month=5, day=10)

    for ticker in tickers:
        run_wide_range(ticker, _from, _to)
        print("________________________")
