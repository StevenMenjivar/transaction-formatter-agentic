from decimal import Decimal
import pytest
from app.services.amount_normalizer import parse_amount

@pytest.mark.parametrize("raw,expected", [("100.50", Decimal("100.50")), ("€99,99", Decimal("99.99")), ("1.250,75", Decimal("1250.75")), ("1,250.75", Decimal("1250.75")), ("-10.25", Decimal("-10.25")), (0, Decimal("0")), (10050, Decimal("10050"))])
def test_parse_amount(raw, expected):
    assert parse_amount(raw)[0] == expected

def test_invalid_amount():
    with pytest.raises(ValueError):
        parse_amount("not-money")
