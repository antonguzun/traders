from dataclasses import dataclass
from datetime import datetime
from typing import Callable, List, Optional, Type, Union

from app.clients.base import BaseClient
from app.settings import DATA_DIR
from sim import (
    Baffett,
    OnePaperHistoryRunDayBreakoutTrader,
    OnePaperHistoryWideRangeTrader,
)
from sim.base import BaseTrader, OnePaperHistoryBaseTrader
from sim.constants import TICKERS
from sim.models import DealsView
from sim.utils.params_finder import find_days_breakout_params, find_wide_range_params


@dataclass
class TraderSimParams:
    name: str
    trader_class: Type[Union[BaseTrader, OnePaperHistoryBaseTrader]]
    find_params: Optional[Callable]


class CsvSaver:
    """Класс отвечает за запись в csv"""

    dir_name = "summary"

    def __init__(self, filename: str, dir_name: str = "summary"):
        self.filename = DATA_DIR / dir_name / filename

    def _save_row(self, data: List[str]):
        content = ",".join(data) + "\n"
        with open(self.filename, "a") as file:
            file.write(content)

    def init_header(self, trader_names: List[str]):
        data = ["ticker", *trader_names]
        self._save_row(data)

    def save_ticker_result(self, ticker: str, results: List[str]):
        data = [ticker, *results]
        self._save_row(data)


class SummaryTradeResultsCsvSaver:
    """с помощью client получаем данные по тикерам и итеративно вычисляем результат
    для каждого Трейдера, указанного в traders_resources"""

    client: BaseClient
    csv_saver: CsvSaver
    traders_resources: List[TraderSimParams]

    def __init__(
        self,
        client: BaseClient,
        csv_saver: CsvSaver,
        traders_resources: List[TraderSimParams],
    ):
        self.client = client
        self.csv_saver = csv_saver
        self.traders_resources = traders_resources

    @staticmethod
    def result_by_trader(trader_resources, candles) -> str:
        if trader_resources.find_params:
            best_params = trader_resources.find_params(candles.copy())
            trader = trader_resources.trader_class(best_params)
        else:
            trader = trader_resources.trader_class()
        deals = trader.create_deals(candles.copy())
        if not deals:
            return "N/A"
        deals_view = DealsView(deals, candles[0].close)
        return str(deals_view.total_result_in_proc)

    def save_trade_results(self, tickers: List[str], _from: datetime, _to: datetime):
        names = [trader_resources.name for trader_resources in self.traders_resources]
        self.csv_saver.init_header(names)

        for ticker in tickers:
            candles = self.client.get_candles_by_ticker(ticker, _from, _to)
            results = []
            for trader_resources in self.traders_resources:
                result = self.result_by_trader(trader_resources, candles)
                results.append(result)
            self.csv_saver.save_ticker_result(ticker, results)
            print(f"ticker {ticker} saved")

    def __call__(self, tickers: List[str], _from: datetime, _to: datetime):
        self.save_trade_results(tickers, _from, _to)


if __name__ == "__main__":
    from app.clients.tinkoff import TIClient
    from app.settings import TINKOFF_SANDBOX_TOKEN

    _from = datetime(year=2020, month=5, day=10)
    _to = datetime(year=2021, month=5, day=10)

    params = {
        "client": TIClient(TINKOFF_SANDBOX_TOKEN, use_sandbox=True),
        "csv_saver": CsvSaver(f"{_from.date()}_to_{_to.date()}.csv", "summary"),
        "traders_resources": [
            TraderSimParams("ref", Baffett, None),
            TraderSimParams(
                "wide_range", OnePaperHistoryWideRangeTrader, find_wide_range_params
            ),
            TraderSimParams(
                "run_days_breakout",
                OnePaperHistoryRunDayBreakoutTrader,
                find_days_breakout_params,
            ),
        ],
    }
    save_csv = SummaryTradeResultsCsvSaver(**params)
    save_csv(tickers=TICKERS, _from=_from, _to=_to)
