from datetime import datetime, date, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from dateutil import parser as date_parser
from app.core.config import settings

FORMATS = [
    "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M", "%Y-%m-%d", "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M", "%m/%d/%Y %H:%M:%S", "%m/%d/%Y %H:%M",
    "%d/%m/%Y", "%m/%d/%Y",
]

def normalize_date(value, timezone_name=None, date_order=None):
    if value in (None, ""):
        return None, None
    tz_name = timezone_name or settings.timezone
    order = (date_order or settings.date_order).upper()
    try:
        target_tz = ZoneInfo(tz_name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Zona horaria no válida: {tz_name}") from exc
    parsed = None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        # Numeric timestamps are interpreted as Unix seconds; milliseconds are detected.
        timestamp = float(value) / 1000 if abs(float(value)) > 100_000_000_000 else float(value)
        parsed = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    elif isinstance(value, datetime):
        parsed = value
    elif isinstance(value, date):
        parsed = datetime(value.year, value.month, value.day)
    elif isinstance(value, str):
        text = value.strip()
        for fmt in FORMATS:
            try:
                # Only try DMY/MM formats matching configured order for ambiguous numeric dates.
                if "%d/%m/%Y" in fmt and order != "DMY":
                    continue
                if "%m/%d/%Y" in fmt and order != "MDY":
                    continue
                parsed = datetime.strptime(text, fmt)
                break
            except ValueError:
                pass
        if parsed is None:
            try:
                parsed = date_parser.parse(text, dayfirst=(order == "DMY"), yearfirst=False, fuzzy=False)
            except (ValueError, OverflowError) as exc:
                return None, f"No se pudo interpretar la fecha: {value!r}."
    else:
        return None, f"Tipo de fecha no compatible: {type(value).__name__}."
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=target_tz)
    else:
        parsed = parsed.astimezone(target_tz)
    return parsed.isoformat(timespec="seconds"), None
