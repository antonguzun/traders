import datetime

from tinvest import SyncClient, CandleResolution

from tests.test_wide_ranging_day_bot import OnePaperHistoryWideRangeTrader, cals_passive_profit
from app.settings import TINKOFF_SANDBOX_TOKEN


def run_wide_range(tiket: str):
    client = SyncClient(TINKOFF_SANDBOX_TOKEN, use_sandbox=True)
    instrument_figi = client.get_market_search_by_ticker(tiket).payload.instruments[0].figi

    res = CandleResolution.day
    _from = datetime.datetime(year=2020, month=5, day=10)
    _to = datetime.datetime(year=2021, month=5, day=10)
    c = client.get_market_candles(instrument_figi, _from, _to, res)
    print(f"TIKET {tiket}")
    print(f"date range: from {_from} to {_to}")

    trader = OnePaperHistoryWideRangeTrader()
    passive_profit = cals_passive_profit(c.payload.candles)
    active_profit = trader.calc_active_profit(c.payload.candles)
    active_effect = active_profit - passive_profit

    print(f"profit passive {round(passive_profit)}%")
    print(f"profit active {round(active_profit)}%")
    print(f"profit effect {round(active_effect)}%")


if __name__ == "__main__":
    tikets = ["TMOS", "FXIM", "TSPX", "TECH"]
    for tiket in tikets:
        run_wide_range(tiket)
        print("________________________")
