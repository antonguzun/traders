from datetime import datetime

from app.clients.tinkoff import TIClient
from app.settings import TINKOFF_SANDBOX_TOKEN
from bots.run_day_breakout_bot.models import RunDayBreakoutParams
from sim.traders import OnePaperHistoryRunDayBreakoutTrader
from sim.utils.printers import TradingPrinter

if __name__ == "__main__":
    client = TIClient(TINKOFF_SANDBOX_TOKEN, use_sandbox=True)
    trader = OnePaperHistoryRunDayBreakoutTrader(
        RunDayBreakoutParams(3, 3), is_short_on=True
    )
    print_trade_results = TradingPrinter(client, trader)

    print_trade_results(
        ticker="AMD",
        _from=datetime(year=2020, month=5, day=10),
        _to=datetime(year=2021, month=5, day=10),
    )
