from decimal import Decimal, InvalidOperation
import re
from app.core.constants import CURRENCY_SYMBOLS

ISO_RE = re.compile(r"(?<![A-Za-z])[A-Za-z]{3}(?![A-Za-z])")

def parse_amount(value):
    if isinstance(value, bool) or value is None:
        raise ValueError("El monto está vacío o no es numérico.")
    if isinstance(value, (int, float, Decimal)):
        try:
            return Decimal(str(value)), None, None
        except InvalidOperation as exc:
            raise ValueError("El monto no es numérico.") from exc
    if not isinstance(value, str):
        raise ValueError("El tipo de dato del monto no es compatible.")
    text = value.strip().replace("\u00a0", " ")
    if not text:
        raise ValueError("El monto está vacío.")
    iso_match = ISO_RE.search(text)
    embedded_iso = iso_match.group(0).upper() if iso_match else None
    for code in (embedded_iso,):
        if code and len(code) != 3:
            embedded_iso = None
    symbol_currency = None
    for symbol, currency in CURRENCY_SYMBOLS.items():
        if symbol in text:
            symbol_currency = currency
            break
    cleaned = ISO_RE.sub("", text)
    for symbol in CURRENCY_SYMBOLS:
        cleaned = cleaned.replace(symbol, "")
    cleaned = re.sub(r"[^0-9,\.\-+()]", "", cleaned)
    if cleaned.startswith("(") and cleaned.endswith(")"):
        cleaned = "-" + cleaned[1:-1]
    if not cleaned or cleaned in {"-", "+", ".", ","}:
        raise ValueError("No se pudo extraer un valor numérico del monto.")
    if "," in cleaned and "." in cleaned:
        # Last separator is decimal; the other is treated as grouping.
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        pieces = cleaned.split(",")
        if len(pieces) > 2 or (len(pieces[-1]) == 3 and len(pieces[0].lstrip("+-")) >= 1):
            cleaned = "".join(pieces)
        else:
            cleaned = cleaned.replace(",", ".")
    elif cleaned.count(".") > 1:
        pieces = cleaned.split(".")
        cleaned = "".join(pieces[:-1]) + "." + pieces[-1]
    try:
        amount = Decimal(cleaned)
    except InvalidOperation as exc:
        raise ValueError(f"Formato de monto no reconocido: {value!r}") from exc
    return amount, embedded_iso, symbol_currency
