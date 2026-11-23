import json
from decimal import Decimal


def dumps_decimal(value, indent=2, ensure_ascii=False):
    """Serialize Decimal values as JSON numbers without converting them to float."""
    def encode(item, level=0):
        if isinstance(item, Decimal):
            if not item.is_finite():
                raise ValueError("JSON no admite Decimal no finitos.")
            return format(item, "f")
        if isinstance(item, dict):
            if not item:
                return "{}"
            pad = " " * (indent * (level + 1)) if indent is not None else ""
            close_pad = " " * (indent * level) if indent is not None else ""
            separator = ": " if indent is not None else ":"
            parts = [pad + json.dumps(str(k), ensure_ascii=ensure_ascii) + separator + encode(v, level + 1)
                     for k, v in item.items()]
            joiner = ",\n" if indent is not None else ","
            return "{\n" + joiner.join(parts) + "\n" + close_pad + "}" if indent is not None else "{" + joiner.join(parts) + "}"
        if isinstance(item, (list, tuple)):
            if not item:
                return "[]"
            pad = " " * (indent * (level + 1)) if indent is not None else ""
            close_pad = " " * (indent * level) if indent is not None else ""
            joiner = ",\n" if indent is not None else ","
            parts = [pad + encode(v, level + 1) for v in item]
            return "[\n" + joiner.join(parts) + "\n" + close_pad + "]" if indent is not None else "[" + joiner.join(parts) + "]"
        return json.dumps(item, ensure_ascii=ensure_ascii, separators=(",", ":"))
    return encode(value)
