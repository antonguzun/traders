from datetime import datetime

from bots.wide_ranging_day_bot.models import StrategyParams
from sim import OnePaperHistoryWideRangeTrader


def gen_params():
    for j in range(10, 25):
        for i in range(0, 7):
            yield StrategyParams(i, j / 10)


def find_params(candles) -> StrategyParams:
    profit = 0
    best_params = None
    for params in gen_params():
        trader = OnePaperHistoryWideRangeTrader(params, is_short_on=True)
        local_profit = sum(trader.create_deals(candles))
        if local_profit > profit:
            profit = local_profit
            best_params = params
    return best_params


def save_params(ticker: str, params: StrategyParams, profit_proc, profit_effect, from_dt: datetime, to_dt: datetime):
    from app.settings import DATA_DIR

    filepath = DATA_DIR / "wide_range" / f"{from_dt.date()}_to_{to_dt.date()}.csv"

    with open(filepath, "a") as file:
        file.write(f"{ticker},{profit_proc},{profit_effect},{params.n1},{params.k}\n")


def run_for_tickers():
    from sim.constants import TICKERS
    from app.settings import TINKOFF_SANDBOX_TOKEN
    from tinvest import CandleResolution
    from sim import Baffett
    from sim.models import DealsView
    from tinvest import SyncClient
    for ticker in TICKERS:
        client = SyncClient(TINKOFF_SANDBOX_TOKEN, use_sandbox=True)
        instrument_figi = client.get_market_search_by_ticker(ticker).payload.instruments[0].figi

        res = CandleResolution.day
        _from = datetime(year=2020, month=5, day=10)
        _to = datetime(year=2021, month=5, day=10)
        candles = client.get_market_candles(instrument_figi, _from, _to, res).payload.candles

        params = find_params(candles.copy())
        trader = OnePaperHistoryWideRangeTrader(params, is_short_on=True)
        active_deals = trader.create_deals(candles)
        passive_deals = Baffett().create_deals(candles)

        active_deals_view = DealsView(active_deals, candles[0].c)
        passive_deals_view = DealsView(passive_deals, candles[0].c)
        effect = round(active_deals_view.total_result_in_proc - passive_deals_view.total_result_in_proc, 2)
        print(f"{ticker}: n1: {params.n1}, k: {params.k}, effect: {effect}")
        save_params(ticker, params, active_deals_view.total_result_in_proc, effect, _from, _to)


if __name__ == "__main__":
    run_for_tickers()