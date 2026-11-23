from app.services.date_normalizer import normalize_date

def test_iso_date():
    value, warning = normalize_date("2025-03-10T14:22:00Z", "UTC", "DMY")
    assert value == "2025-03-10T14:22:00+00:00" and warning is None

def test_dmy_date():
    value, warning = normalize_date("10/03/2025 14:22", "UTC", "DMY")
    assert value.startswith("2025-03-10T14:22:00") and warning is None

def test_missing_date():
    value, warning = normalize_date(None)
    assert value is None and warning is None
