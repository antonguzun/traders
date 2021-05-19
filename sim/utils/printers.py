from datetime import datetime

from app.clients.base import BaseClient
from sim import Baffett
from sim.base import BaseTrader
from sim.models import DealsView


class TradingPrinter:
    client: BaseClient
    ref_trader: BaseTrader
    trader: BaseTrader

    def __init__(
        self, client: BaseClient, trader: BaseTrader, ref_trader: BaseTrader = Baffett()
    ):
        self.client = client
        self.trader = trader
        self.ref_trader = ref_trader

    def print_history_trading(self, ticker: str, _from: datetime, _to: datetime):
        candles = self.client.get_candles_by_ticker(ticker, _from, _to)

        active_deals = self.trader.create_deals(candles)
        passive_deals = self.ref_trader.create_deals(candles)

        active_deals_view = DealsView(active_deals, candles[0].close)
        passive_deals_view = DealsView(passive_deals, candles[0].close)
        effect = round(
            active_deals_view.total_result_in_proc
            - passive_deals_view.total_result_in_proc,
            2,
        )

        print(f"TICKER {ticker}")
        print(f"date range: from {candles[0].time.date()} to {candles[-1].time.date()}")
        print("active deals:", *active_deals, sep="\n")
        print(f"profit active {active_deals_view}")
        print(f"profit passive {passive_deals_view}")
        print(f"profit effect {effect}%")
        print("________________________")
