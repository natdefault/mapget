import re

from github import MappingGitHub

from utils.compare import (
    readable_name,
    external_info,
    version_unavailable_mapping
)


class MappingManager:
    def __init__(self):
        self.github = MappingGitHub()

    def handle_query(self, query, mapping_type, version, progress_callback=None):
        if not query:
            return "Empty query"

        query = query.strip()

        if mapping_type == "auto":
            mapping_type = self.detect_mapping_type(query)

        result = self.github.search(
            query,
            mapping_type,
            version,
            progress_callback=progress_callback
        )

        if not result:
            return "Search failed"

        if "error" in result or "reason" in result:
            index = self.github.get_index(
                mapping_type,
                version,
                progress_callback=progress_callback
            )

            sample_keys = []

            if isinstance(index, dict):
                sample_keys = list(index.keys())[:20]

            return (
                f"Mapping: {mapping_type}\n\n"
                f"ERROR: {result.get('error') or result.get('reason')}\n"
                f"Query: {query}\n"
                f"Version: {version}\n\n"
                f"Index loaded: {index is not None}\n"
                f"Index size: {len(index) if isinstance(index, dict) else 0}\n"
                f"Sample keys: {sample_keys}\n"
            )

        readable = result.get("readable")

        if not readable:
            readable = readable_name(result)

        hint = result.get("hint")

        if not hint:
            hint = external_info(result)

        unavailable_text = version_unavailable_mapping(
            mapping_type,
            version,
            result.get("reason") or result.get("error")
        )

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
            f"Descriptor: {result.get('descriptor')}\n"
            f"Path: {result.get('path')}\n"
            f"Source Mapping: {result.get('source_mapping', mapping_type)}\n"
            f"Type: {result.get('type')}\n"
            f"Category: {result.get('category')}\n"
            f"Version: {result.get('version')}\n"
            f"Extra: {result.get('extra', '')}\n"
            f"Hint: {hint if hint else 'No extra hints available'}\n"
        )

    def detect_mapping_type(self, query):
        query = query.strip()

        if re.match(r"^[a-z]{1,3}$", query):
            return "obfuscated"

        if re.match(r"^class_\d+$", query):
            return "intermediary"

        if re.match(r"^method_\d+$", query):
            return "intermediary"

        if re.match(r"^field_\d+$", query):
            return "intermediary"

        if re.match(r"^func_\d+_[a-zA-Z_]+$", query):
            return "srg"

        if re.match(r"^field_\d+_[a-zA-Z_]+$", query):
            return "srg"

        if query.startswith("net.minecraft"):
            return "mojmap"

        if "/" in query:
            return "yarn"

        if "." in query:
            return "mojmap"

        return "mojmap"