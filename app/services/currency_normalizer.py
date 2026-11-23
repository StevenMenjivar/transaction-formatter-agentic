import pycountry

def valid_iso(code):
    if not isinstance(code, str):
        return None
    code = code.strip().upper()
    return code if len(code) == 3 and pycountry.currencies.get(alpha_3=code) else None

def normalize_currency(explicit_value, embedded_iso=None, symbol_currency=None):
    explicit = valid_iso(str(explicit_value)) if explicit_value not in (None, "") else None
    embedded = valid_iso(embedded_iso)
    warnings = []
    if explicit:
        if embedded and embedded != explicit:
            warnings.append(f"La moneda explícita ({explicit}) contradice el código del monto ({embedded}); prevalece la explícita.")
        return explicit, warnings
    if embedded:
        return embedded, warnings
    if symbol_currency:
        # Symbols with a unique mapping in our conservative map can be used;
        # ambiguous symbols are deliberately left unknown.
        return valid_iso(symbol_currency), warnings
    if explicit_value not in (None, ""):
        warnings.append(f"Código de moneda no reconocido: {explicit_value!r}.")
    return None, warnings
