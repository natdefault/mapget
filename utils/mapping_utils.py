import re

PLACEHOLDER_RE = re.compile(r"^(field_|func_|method_)\d+$")


def is_placeholder(name):
    if not name:
        return False
    return bool(PLACEHOLDER_RE.match(name))


def readable_name(name):
    if not name:
        return None
    if is_placeholder(name):
        return None
    return name


def hint_for_entry(entry):
    if not isinstance(entry, dict):
        return None

    typ = entry.get("type", "")
    cls = entry.get("class", "") or entry.get("path", "") or ""

    if typ == "field":
        if ".Blocks" in cls or cls.endswith("Blocks"):
            return "Block constant field; readable name unavailable in current mapping"
        if ".Items" in cls or cls.endswith("Items") or ".Item" in cls:
            return "Item constant field; readable name unavailable in current mapping"
        if "Block" in cls or "block" in cls:
            return "Block-related field; readable name unavailable in current mapping"
    if typ == "method":
        return "Method placeholder; actual method name unavailable in this mapping"
    if typ == "class":
        return None

    if is_placeholder(entry.get("named")):
        return "Placeholder name detected; readable mapping not available"
    return None
