import requests
import os
import json
import zipfile
import io

from parsers.mojmap import MojmapParser
from parsers.mcp import MCPParser
from parsers.Yarn import YarnParser
from utils.mapping_utils import is_placeholder, readable_name, hint_for_entry


class MappingGitHub:
    def __init__(self):
        self.cache = {}
        self.cache_dir = "cache"
        os.makedirs(self.cache_dir, exist_ok=True)

    def _cache_path(self, mapping_type, version):
        return os.path.join(self.cache_dir, f"{mapping_type}_{version}.json")

    def load_cache(self, mapping_type, version):
        path = self._cache_path(mapping_type, version)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def save_cache(self, mapping_type, version, data):
        with open(self._cache_path(mapping_type, version), "w", encoding="utf-8") as f:
            json.dump(data, f)

    def _is_valid_index(self, index):
        if not isinstance(index, dict):
            return False

        for value in index.values():
            if not isinstance(value, dict):
                return False
            if "type" not in value:
                return False
            if "path" not in value and "obf" not in value and "intermediary" not in value:
                return False

        return True

    def fetch_version_manifest(self):
        url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json" # ?????
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None

    def get_version_json(self, version):
        manifest = self.fetch_version_manifest()
        if not manifest:
            return None

        for v in manifest["versions"]:
            if v["id"] == version:
                r = requests.get(v["url"])
                return r.json() if r.status_code == 200 else None

        return None

    def fetch_mojmap(self, version):
        data = self.get_version_json(version)
        if not data:
            return None

        downloads = data.get("downloads", {})
        mappings = downloads.get("client_mappings") or downloads.get("server_mappings")
        if not mappings:
            return None

        r = requests.get(mappings["url"])
        return r.text if r.status_code == 200 else None

    #mcp github :sob:
    def fetch_mcp(self, version):
        url = f"https://raw.githubusercontent.com/MinecraftForge/MCPConfig/master/versions/{version}/joined.srg"
        r = requests.get(url)
        return r.text if r.status_code == 200 else None

    def _normalize_yarn_version(self, version):
        if "+build." in version:
            return version

        url = f"https://meta.fabricmc.net/v2/versions/yarn/{version}"
        r = requests.get(url)
        if r.status_code != 200:
            return None

        versions = r.json()
        if isinstance(versions, dict):
            versions = [versions]
        if not versions:
            return None

        versions.sort(key=lambda item: (item.get("stable", False), item.get("build", 0)), reverse=True)
        return versions[0].get("version")

    def fetch_yarn(self, version):
        yarn_version = self._normalize_yarn_version(version)
        if not yarn_version:
            return None

        url = f"https://maven.fabricmc.net/net/fabricmc/yarn/{yarn_version}/yarn-{yarn_version}.jar"
        r = requests.get(url)
        if r.status_code != 200:
            return None

        with io.BytesIO(r.content) as jar_data:
            with zipfile.ZipFile(jar_data) as zf:
                for name in zf.namelist():
                    if name.lower().endswith(".tiny"):
                        return zf.read(name).decode("utf-8")

        return None

    def is_mcp_version_allowed(self, version):
        try:
            major, minor = map(int, version.split(".")[:2])
            return major == 1 and minor <= 12
        except Exception:
            return False

    def get_index(self, mapping_type, version):
        if mapping_type == "obfuscated":
            return None

        key = f"{mapping_type}_{version}"
        if key in self.cache:
            return self.cache[key]

        cached = self.load_cache(mapping_type, version)
        if cached and self._is_valid_index(cached):
            self.cache[key] = cached
            return cached

        if mapping_type == "mojmap":
            raw = self.fetch_mojmap(version)
            if not raw:
                return None
            index = MojmapParser().parse(raw)

        elif mapping_type == "mcp":
            if not self.is_mcp_version_allowed(version):
                return {"_invalid": True, "reason": "MCP only supports <= 1.12.x"}
            raw = self.fetch_mcp(version)
            if not raw:
                return None
            index = MCPParser().parse(raw)

        elif mapping_type == "yarn":
            raw = self.fetch_yarn(version)
            if not raw:
                return None
            index = YarnParser().parse(raw)

        else:
            return None

        self.cache[key] = index
        self.save_cache(mapping_type, version, index)
        return index


    def search(self, query, mapping_type, version):
        if mapping_type == "obfuscated":
            return self._search_obfuscated(query, version)

        index = self.get_index(mapping_type, version)
        if not index:
            return {"error": "Index failed to load"}
        if isinstance(index, dict) and index.get("_invalid"):
            return index

        if mapping_type == "mcp":
            return self._search_mcp(index, query, version)

        result = self._search_index(index, query, version, mapping_type)
        if result:
            return result

        return {
            "error": f"Query not found in {mapping_type.capitalize()}",
            "query": query,
        }

    def _search_obfuscated(self, query, version):
        for mapping_type in ["yarn", "mojmap", "mcp"]:
            index = self.get_index(mapping_type, version)
            if not index or (isinstance(index, dict) and index.get("_invalid")):
                continue
            result = self._search_index(index, query, version, mapping_type)
            if result:
                result["mapping"] = "obfuscated"
                result["source_mapping"] = mapping_type
                readable = self._find_readable_name(result, version)
                if readable:
                    result["readable"] = readable
                return result

        return {
            "error": "Query not found in obfuscated search",
            "query": query,
        }

    def _search_index(self, index, query, version, mapping_type):
        if query in index:
            return self._resolve_output(query, index[query], version, mapping_type)

        lower_query = query.lower()
        for key, value in index.items():
            if lower_query in key.lower():
                return self._resolve_output(key, value, version, mapping_type)
            if lower_query in str(value.get("named", "")).lower():
                return self._resolve_output(key, value, version, mapping_type)
            if lower_query in str(value.get("intermediary", "")).lower():
                return self._resolve_output(key, value, version, mapping_type)
            if lower_query in str(value.get("path", "")).lower():
                return self._resolve_output(key, value, version, mapping_type)

        return None

    def _search_mcp(self, index, query, version):
        if query in index:
            return self._resolve_output(query, index[query], version, "mcp")

        lower_query = query.lower()
        for key, value in index.items():
            if lower_query in key.lower() or lower_query in str(value.get("named", "")).lower():
                return self._resolve_output(key, value, version, "mcp")

        return {
            "error": "MCP key not found",
            "query": query,
        }

    def _resolve_output(self, key, data, version, mapping_type):
        name = data.get("named") or data.get("intermediary") or data.get("path") or key
        resolved = data.get("path") or data.get("named") or data.get("class") or key
        extra_parts = []

        if "obf" in data:
            extra_parts.append(f"obf={data['obf']}")
        if "intermediary" in data:
            extra_parts.append(f"intermediary={data['intermediary']}")
        if "descriptor" in data:
            extra_parts.append(f"descriptor={data['descriptor']}")
        if data.get("source_mapping"):
            extra_parts.append(f"source={data['source_mapping']}")

        result = {
            "name": key,
            "resolved": resolved,
            "type": data.get("type", mapping_type),
            "category": data.get("type") or self._guess_category(key),
            "version": version,
            "mapping": mapping_type,
            "obfuscated": data.get("obf", key),
            "deobfuscated": name,
            "class": data.get("class"),
            "extra": " ".join(extra_parts),
        }

        readable = readable_name(result["deobfuscated"])
        if readable:
            result["readable"] = readable
        else:
            result["readable"] = self._find_readable_name(result, version) or "Unavailable"
            result["hint"] = hint_for_entry(data)

        return result

    def _find_readable_name(self, result, version):
        if result.get("readable") and result["readable"] != "Unavailable":
            return result["readable"]

        source_mapping = result.get("source_mapping") or result.get("mapping")
        search_types = ["yarn", "mojmap", "mcp"]
        if source_mapping in search_types:
            search_types.remove(source_mapping)
        for mapping_type in search_types:
            index = self.get_index(mapping_type, version)
            if not index or (isinstance(index, dict) and index.get("_invalid")):
                continue

            obf = result.get("obfuscated")
            if obf and obf in index:
                candidate = index[obf].get("named") or index[obf].get("intermediary")
                if candidate and not is_placeholder(candidate):
                    return candidate

            path = result.get("resolved")
            if path and path in index:
                candidate = index[path].get("named") or index[path].get("intermediary")
                if candidate and not is_placeholder(candidate):
                    return candidate

        return None

    def _guess_category(self, key):
        if "field_" in key:
            return "field"
        if "func_" in key or "method_" in key:
            return "method"
        return "class"
    
    #hmmm i wonder what that does
