import re
import unicodedata
from difflib import SequenceMatcher
from app.core.constants import FIELD_ALIASES
from app.core.config import settings

CONTAINER_KEYS = {"metadata", "meta", "headers", "pagination", "links", "summary"}

def normalize_key(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]", "", value.lower())

def walk_properties(obj, path=(), depth=0):
    if not isinstance(obj, dict) or depth > settings.max_depth:
        return
    for key, value in obj.items():
        current = path + (str(key),)
        yield str(key), value, current, depth
        if isinstance(value, dict):
            yield from walk_properties(value, current, depth + 1)

def detect_fields(record: dict):
    found = {}
    for key, value, path, depth in walk_properties(record):
        nk = normalize_key(key)
        if not nk:
            continue
        for field, aliases in FIELD_ALIASES.items():
            if nk in aliases:
                found.setdefault(field, []).append({"field": field, "key": key, "value": value,
                    "path": ".".join(path), "priority": aliases[nk], "method": "exact"})
                continue
            # Conservative fuzzy matching against known aliases only.
            best = max((SequenceMatcher(None, nk, alias).ratio(), alias, rank)
                       for alias, rank in aliases.items())
            score, alias, rank = best
            if score >= settings.fuzzy_threshold and len(nk) >= 5:
                found.setdefault(field, []).append({"field": field, "key": key, "value": value,
                    "path": ".".join(path), "priority": rank + 100, "method": f"fuzzy:{score:.2f}"})
    for field, candidates in found.items():
        candidates.sort(key=lambda c: (c["priority"], c["path"].count("."), c["path"]))
    return found

def looks_like_transaction(obj: dict) -> bool:
    detected = detect_fields(obj)
    return bool(detected.get("amount") or detected.get("originalReference") or detected.get("transactionDate"))
