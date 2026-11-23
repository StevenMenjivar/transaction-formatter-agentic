"""Caso de uso de normalización: compone descubrimiento, normalización y métricas."""
from collections import Counter
from app.core.config import settings
from app.services.record_discovery import _discover_records
from app.services.transaction_normalizer import process_transaction

def process_payload(payload, timezone_name=None, date_order=None):
    records = _discover_records(payload)
    if not records:
        raise ValueError("No se encontraron transacciones en la estructura JSON proporcionada.")
    if len(records) > settings.max_transactions:
        raise ValueError(f"El documento supera el máximo permitido de {settings.max_transactions} elementos.")
    valid, invalid, details = [], [], []
    warning_count = 0
    for position, (record, source_path) in enumerate(records, start=1):
        if not isinstance(record, dict):
            invalid_item = {"position": position, "sourcePath": source_path, "original": record,
                            "errors": ["El elemento no es un objeto JSON."], "warnings": [], "trace": {}}
            invalid.append(invalid_item)
            continue
        normalized, detail = process_transaction(record, position, len(valid) + 1, timezone_name, date_order)
        detail["sourcePath"] = source_path
        if normalized is None:
            invalid.append(detail)
        else:
            valid.append(normalized)
            details.append({"id": normalized["id"], "original": record, **detail})
            warning_count += bool(detail["warnings"])
    status_counts = dict(Counter(x["status"] for x in valid))
    currency_counts = dict(Counter(x["currency"] or "UNKNOWN" for x in valid))
    dates_unavailable = sum(1 for x in valid if x["transactionDate"] is None)
    unknown_currency = sum(1 for x in valid if x["currency"] is None)
    total = len(records)
    valid_count, invalid_count = len(valid), len(invalid)
    metrics = {
        "processed": total, "valid": valid_count, "invalid": invalid_count,
        "validPercentage": round(valid_count * 100 / total, 2) if total else 0,
        "invalidPercentage": round(invalid_count * 100 / total, 2) if total else 0,
        "withWarnings": int(warning_count), "unknownCurrency": unknown_currency,
        "unavailableDates": dates_unavailable,
        "statusCounts": status_counts, "currencyCounts": currency_counts,
    }
    return {"transactions": valid, "invalidTransactions": invalid, "details": details, "metrics": metrics}
