"""Normalización determinista de un registro transaccional."""
from app.services.field_detector import detect_fields
from app.services.amount_normalizer import parse_amount
from app.services.currency_normalizer import normalize_currency
from app.services.date_normalizer import normalize_date
from app.services.status_normalizer import normalize_status
from app.models.transaction import NormalizedTransaction

def _selected(found, field):
    candidates = found.get(field, [])
    return candidates[0] if candidates else None

def _different(candidates):
    values = []
    for item in candidates:
        value = item["value"]
        if isinstance(value, (dict, list)):
            value = repr(value)
        values.append(str(value).strip())
    return len(set(values)) > 1

def _warn_conflicts(found, warnings):
    for field, candidates in found.items():
        if len(candidates) > 1 and _different(candidates):
            chosen = candidates[0]
            warnings.append({"code": "FIELD_CONFLICT", "field": field,
                "message": f"Se encontraron propiedades candidatas contradictorias para {field}; prevalece {chosen['path']}.",
                "candidates": [{"path": c["path"], "value": c["value"]} for c in candidates]})

def process_transaction(record, position, normalized_id, timezone_name=None, date_order=None):
    found = detect_fields(record)
    warnings = []
    _warn_conflicts(found, warnings)
    trace = {}
    for field in ("amount", "currency", "transactionDate", "status", "originalReference", "concept"):
        candidate = _selected(found, field)
        trace[field] = ({"path": candidate["path"], "sourceKey": candidate["key"],
                         "originalValue": candidate["value"], "method": candidate["method"]}
                        if candidate else None)

    amount_candidate = _selected(found, "amount")
    if not amount_candidate:
        return None, {"position": position, "original": record, "errors": ["No se encontró una propiedad válida de monto."], "warnings": warnings, "trace": trace}
    try:
        amount, embedded_iso, symbol_currency = parse_amount(amount_candidate["value"])
    except ValueError as exc:
        return None, {"position": position, "original": record, "errors": [str(exc)], "warnings": warnings, "trace": trace}

    currency_candidate = _selected(found, "currency")
    currency_value = currency_candidate["value"] if currency_candidate else None
    currency, currency_warnings = normalize_currency(currency_value, embedded_iso, symbol_currency)
    for message in currency_warnings:
        warnings.append({"code": "CURRENCY_WARNING", "field": "currency", "message": message})

    date_candidate = _selected(found, "transactionDate")
    date_value = date_candidate["value"] if date_candidate else None
    transaction_date, date_warning = normalize_date(date_value, timezone_name, date_order)
    if date_warning:
        warnings.append({"code": "DATE_WARNING", "field": "transactionDate", "message": date_warning})

    status_candidate = _selected(found, "status")
    status = normalize_status(status_candidate["value"] if status_candidate else None)
    ref_candidate = _selected(found, "originalReference")
    reference = ref_candidate["value"] if ref_candidate else None
    if reference is not None:
        if isinstance(reference, (dict, list)):
            reference = str(reference)
        else:
            reference = str(reference)
    concept_candidate = _selected(found, "concept")
    concept = concept_candidate["value"] if concept_candidate else None
    if concept is not None and not isinstance(concept, str):
        concept = str(concept)

    result = NormalizedTransaction(
        id=normalized_id, amount=amount, currency=currency,
        transactionDate=transaction_date, status=status,
        originalReference=reference, concept=concept,
    ).model_dump()
    return result, {"position": position, "warnings": warnings, "trace": trace}

