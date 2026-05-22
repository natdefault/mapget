import re

PLACEHOLDER_RE = re.compile(r"^(?:field_|method_|func_)\d+$", re.IGNORECASE)


def is_placeholder_name(name):
    if not name:
        return False
    return bool(PLACEHOLDER_RE.match(name))


def readable_name(result):
    name = result.get("deobfuscated") or result.get("name")
    if not name:
        return "Unavailable"

    if is_placeholder_name(name):
        return "Unavailable"

    return name


def external_info(result):
    cls = result.get("class") or ""
    if cls.endswith(".Blocks"):
        return "Likely a vanilla block constant in Blocks"
    if cls.endswith(".Items"):
        return "Likely a vanilla item constant in Items"
    if cls.endswith(".EntityType"):
        return "Likely a vanilla entity type constant"
    if cls.endswith(".SoundEvents"):
        return "Likely a vanilla sound event constant"
    if cls.endswith(".MobEffects") or cls.endswith(".StatusEffects"):
        return "Likely a vanilla effect constant"
    return "No readable mapping available from available sources"


def version_unavailable_mapping(mapping_type, version, error):
    if mapping_type == "mcp" and error:
        if "MCP only supports" in error:
            return f"Unavailable for {version}"
    return None
