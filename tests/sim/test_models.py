from datetime import datetime
from decimal import Decimal

from sim.models import Deal


def test_deal():
    date = datetime.now()
    deal1 = Deal("KEK", Decimal("1.2"), paper_count=2, date=date)
    deal2 = Deal("KEK", Decimal("3.0"), paper_count=1, date=date)
    deal3 = Deal("KEK", Decimal("0.5"), paper_count=-1, date=date)
    assert round(sum([deal1, deal2, deal3]), 1) == Decimal("-4.9")
