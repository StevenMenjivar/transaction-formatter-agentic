from app.services.transaction_processor import process_payload

def test_total_has_priority_and_invalid_isolated():
    payload = [
        {"amount": "100.00", "total": "250.00", "currency": "USD", "status": "OK"},
        {"status": "pending"},
        "bad-item",
    ]
    result = process_payload(payload)
    assert result["transactions"][0]["amount"] == 250
    assert len(result["transactions"]) == 1
    assert len(result["invalidTransactions"]) == 2
    assert result["metrics"]["processed"] == 3

def test_nested_array():
    result = process_payload({"data": {"transactions": [{"transaction_id": "T1", "amount": 5}]}})
    assert len(result["transactions"]) == 1
    assert result["transactions"][0]["originalReference"] == "T1"
