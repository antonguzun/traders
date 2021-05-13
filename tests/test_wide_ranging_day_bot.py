from decimal import Decimal
from typing import List

from tinvest import Candle

from bots.base_bot import Decision, BaseBot
from bots.wide_ranging_day_bot.bot import WideRangeDayBot


def cals_passive_profit(candles: List[Candle]):
    print(f"profit passive {round(candles[-1].c - candles[0].c, 3)}$")
    return (candles[-1].c - candles[0].c) / candles[0].c * 100


class OnePaperHistoryBaseTrader:
    bot_class = None
    deals_cost = None
    commission_value = Decimal(0.0005)
    papers_count = 0

    def init_bot(self) -> BaseBot:
        return self.bot_class([])

    def make_deal(self, paper_cost, papers_to_deal, date):
        if papers_to_deal == 0:
            return
        papers_to_deal = papers_to_deal
        # При покупке положительное кол-во бумаг и положительная цена приводится к
        # корректной сумме при помощи магической -1
        cost = paper_cost * papers_to_deal * (1 + self.commission_value) * -1
        self.deals_cost.append(cost)
        print(f"{date}: сделка {papers_to_deal} ({paper_cost}), общая стоимость {round(cost, 4)}")
        self.papers_count += papers_to_deal

    def buy(self, candle: Candle):
        papers_to_deal = {0: 1, 1: 0, -1: 2}
        papers_to_deal = papers_to_deal[self.papers_count]
        self.make_deal(candle.c, papers_to_deal, candle.time)

    def sell(self, candle: Candle):
        # papers_to_deal = {0: -1, 1: -2, -1: 0}
        papers_to_deal = {0: 0, 1: -1, -1: 1}  # кейс без шортов ! TODO надо бы переписать эти методы
        papers_to_deal = papers_to_deal[self.papers_count]
        self.make_deal(candle.c, papers_to_deal, candle.time)

    def close_positions(self, candle: Candle):
        papers_to_deal = {0: 0, 1: -1, -1: 1}
        papers_to_deal = papers_to_deal[self.papers_count]
        self.make_deal(candle.c, papers_to_deal, candle.time)

    def calc_active_profit(self, candles: List[Candle]):
        self.deals_cost = []
        generate_signal = self.init_bot()
        for candle in candles:
            decision = generate_signal(candle)
            if decision == Decision.BUY:
                self.buy(candle)
            elif decision == Decision.SELL:
                self.sell(candle)
        self.close_positions(candles[-1])
        print(f"deals count {len(self.deals_cost)}")
        print(f"profit active {round(sum(self.deals_cost), 3)}$")
        return sum(self.deals_cost) / candles[0].c * 100


class OnePaperHistoryWideRangeTrader(OnePaperHistoryBaseTrader):
    bot_class = WideRangeDayBot
