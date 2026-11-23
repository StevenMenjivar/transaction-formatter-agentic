from app.services.currency_normalizer import normalize_currency

def test_explicit_currency_wins():
    code, warnings = normalize_currency("USD", "EUR")
    assert code == "USD" and warnings

def test_ambiguous_dollar_is_unknown():
    assert normalize_currency(None, None, None)[0] is None

def test_iso_code():
    assert normalize_currency(None, "EUR")[0] == "EUR"
