import re
import unicodedata
from app.core.constants import STATUS_MAP

def clean_status(value):
    value = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[\s_-]+", " ", value.strip().lower())

def normalize_status(value):
    if value is None or value == "":
        return "UNKNOWN"
    normalized = clean_status(value)
    for status, values in STATUS_MAP.items():
        if normalized in values:
            return status
    return "UNKNOWN"
