from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List

from sim.constants import COMMISSION_VALUE


@dataclass
class Deal:
    """Класс сделки
    положительное paper_count говорит о факте покупки, отрицательное - о продаже
    price содержит цену одной бумаги без комиссии на момент сделки
    """

    ticker: str
    price: Decimal
    paper_count: int
    date: datetime

    def __str__(self):
        if self.paper_count >= 0:
            action = "buy "
        else:
            action = "sell"
        return (
            f"{self.date.date()}: {action} {abs(self.paper_count)} paper(s) by {self.price}, "
            f" total_cost: {round(self.deal_result, 2)}$"
        )

    @property
    def deal_result(self) -> Decimal:
        """множитель -1 вместе с числом бумаг к сделке (paper_count) формирует итоговую стоимость сделки,
        т.к. price всегда положительный
        -1 бумага * 1$ * 1 приводит к результату +1$, тк продается одна бумага"""
        return self.price * self.paper_count * -1 * (1 + COMMISSION_VALUE)

    def __radd__(self, other: Decimal) -> Decimal:
        """поддерживаем функцию sum()"""
        if other:
            return self.deal_result + other
        return self.deal_result


class DealsView:
    def __init__(self, deals: List[Deal], first_deal_cost: Decimal):
        self.deals = deals
        self.first_deal_cost = first_deal_cost

    def __str__(self):
        if self.deals:
            return (
                f"\tTotal result: \t{self.total_result}$, "
                f"\t{self.total_result_in_proc}%, "
                f"\tdeals count: {len(self.deals)}"
            )
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
