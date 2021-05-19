from typing import List

from app.common.models.candle import Candle

from bots.base_bot import BaseBot, Decision
from sim.constants import COMMISSION_VALUE
from sim.models import Deal


class OnePaperHistoryBaseTrader:
    bot_class = None
    params = None
    deals: List[Deal] = None
    commission_value = COMMISSION_VALUE

    def __init__(self, params=None, is_short_on=False, *args, **kwargs):
        self.is_short_on = is_short_on
        self.params = params

    def init_bot(self) -> BaseBot:
        return self.bot_class(self.params, [])

    @property
    def papers_count(self) -> int:
        return sum([deal.paper_count for deal in self.deals])

    def make_deal(self, candle: Candle, papers_to_deal: int):
        if papers_to_deal == 0:
            return
        deal = Deal(candle.name, candle.close, papers_to_deal, candle.time)
        self.deals.append(deal)

    def buy(self, candle: Candle):
        papers_to_deal_mapping = {0: 1, 1: 0, -1: 2}
        papers_to_deal = papers_to_deal_mapping[self.papers_count]
        self.make_deal(candle, papers_to_deal)

    def sell(self, candle: Candle):
        if self.is_short_on:
            papers_to_deal_mapping = {0: -1, 1: -2, -1: 0}
        else:
            papers_to_deal_mapping = {0: 0, 1: -1, -1: 1}  # !TODO надо бы переписать эти методы
        papers_to_deal = papers_to_deal_mapping[self.papers_count]
        self.make_deal(candle, papers_to_deal)

    def close_positions(self, candle: Candle):
        papers_to_deal_mapping = {0: 0, 1: -1, -1: 1}
        papers_to_deal = papers_to_deal_mapping[self.papers_count]
        self.make_deal(candle, papers_to_deal)

    def create_deals(self, candles: List[Candle]) -> List[Deal]:
        self.deals = []
        generate_signal = self.init_bot()
        for candle in candles:
            decision = generate_signal(candle)
            if decision == Decision.BUY:
                self.buy(candle)
            elif decision == Decision.SELL:
                self.sell(candle)
        self.close_positions(candles[-1])
        return self.deals
