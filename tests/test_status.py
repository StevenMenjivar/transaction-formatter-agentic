from app.services.status_normalizer import normalize_status

def test_status_values():
    assert normalize_status("completed") == "SUCCESS"
    assert normalize_status("No procesada") == "FAILED"
    assert normalize_status("en proceso") == "PENDING"
    assert normalize_status("some-new-state") == "UNKNOWN"
