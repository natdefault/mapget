import re
from github import MappingGitHub
from utils.compare import readable_name, external_info, version_unavailable_mapping


class MappingManager:
    def __init__(self):
        self.github = MappingGitHub()

    def handle_query(self, query, mapping_type, version):
        if not query:
            return "Empty query"

        query = query.strip()

        if mapping_type == "auto":
            mapping_type = self.detect_mapping_type(query)

        result = self.github.search(query, mapping_type, version)

        if "error" in result or "reason" in result:
            index = self.github.get_index(mapping_type, version)

            return (
                f"Mapping: {mapping_type}\n\n"
                f"ERROR: {result.get('error') or result.get('reason')}\n"
                f"Query: {query}\n"
                f"Version: {version}\n\n"
                f"Index loaded: {index is not None}\n"
                f"Index size: {len(index) if isinstance(index, dict) else 0}\n"
                f"Sample keys: {list(index.keys())[:20] if index else []}\n"
            )

        readable = result.get("readable") or readable_name(result)
        hint = result.get("hint") or external_info(result)
        unavailable_text = version_unavailable_mapping(mapping_type, version, result.get("reason") or result.get("error"))
        if unavailable_text:
            readable = f"Unavailable ({unavailable_text})"

        return (
            f"Mapping: {mapping_type}\n\n"
            f"Query: {query}\n"
            f"Name: {result.get('name')}\n"
            f"Readable: {readable}\n"
            f"Resolved: {result.get('resolved')}\n"
            f"Obfuscated: {result.get('obfuscated')}\n"
            f"Deobfuscated: {result.get('deobfuscated')}\n"
            f"Class: {result.get('class')}\n"
            f"Source Mapping: {result.get('source_mapping', mapping_type)}\n"
            f"Type: {result.get('type')}\n"
            f"Category: {result.get('category')}\n"
            f"Version: {result.get('version')}\n"
            f"Extra: {result.get('extra', '')}\n"
            f"Hint: {hint if hint else 'No extra hints available'}\n"
        )

    def detect_mapping_type(self, query):
        if re.match(r"^(field_|func_)\d+", query):
            return "obfuscated"
        if "/" in query or "." in query:
            return "yarn"
        return "mojmap"