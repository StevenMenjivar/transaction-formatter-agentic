"""Detección y recorrido de colecciones transaccionales en documentos JSON."""
from app.core.config import settings
from app.services.field_detector import looks_like_transaction

def _discover_records(payload):
    """Return candidate transaction items, preserving document order and avoiding nested duplicate arrays."""
    found = []
    def visit(node, path=(), depth=0):
        if depth > settings.max_depth:
            return
        if isinstance(node, list):
            dict_items = [x for x in node if isinstance(x, dict)]
            if dict_items and any(looks_like_transaction(x) for x in dict_items):
                for idx, item in enumerate(node):
                    found.append((item, ".".join(map(str, path + (idx,))) or str(idx)))
                return
            for idx, item in enumerate(node):
                visit(item, path + (idx,), depth + 1)
        elif isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, (dict, list)):
                    visit(value, path + (key,), depth + 1)
    # Search transaction arrays first so wrapper metadata (for example a top-level id)
    # is not mistaken for a transaction when a nested transaction collection exists.
    visit(payload)
    if found:
        return found
    if isinstance(payload, dict):
        direct = {"amount", "currency", "transactionDate", "status", "originalReference", "concept"}
        direct_fields = set()
        for key in payload:
            from app.services.field_detector import normalize_key
            nk = normalize_key(key)
            for field, aliases in __import__("app.core.constants", fromlist=["FIELD_ALIASES"]).FIELD_ALIASES.items():
                if nk in aliases:
                    direct_fields.add(field)
        if direct_fields:
            return [(payload, "root")]
    return found

