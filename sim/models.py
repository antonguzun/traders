from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List

from sim.constants import COMMISSION_VALUE


@dataclass
class Deal:
    ticker: str
    price: Decimal
    paper_count: int
    date: datetime

    def __str__(self):
        if self.paper_count >= 0:
            action = "buy "
        else:
            action = "sell"
        return f"deal: {action} {abs(self.paper_count)} paper(s) by {self.price}, " \
               f" total_cost: {round(self.total_deal_cost, 2)}$)"

    @property
    def total_deal_cost(self) -> Decimal:
        return self.price * self.paper_count * -1 * (1 + COMMISSION_VALUE)

    def __radd__(self, other: Decimal) -> Decimal:
        if other:
            return self.total_deal_cost + other
        return self.total_deal_cost


class DealsView:
    def __init__(self, deals: List[Deal], first_deal_cost: Decimal):
        self.deals = deals
        self.first_deal_cost = first_deal_cost

    def __str__(self):
        if self.deals:
            return f"\tTotal result: \t{self.total_result}$, " \
                   f"\t{self.total_result_in_proc}%, " \
                   f"\tdeals count: {len(self.deals)}"
        return "No deals"

    @property
    def total_result(self) -> Decimal:
        return round(sum(self.deals), 2)

    @property
    def total_result_in_proc(self) -> Decimal:
        if self.deals:
            return round(self.total_result / self.first_deal_cost * 100, 2)
        else:
            return Decimal("0.0")
