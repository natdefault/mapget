import requests
import os
import sqlite3
import pickle
import zlib
import zipfile
import io
import json

from parsers.mojmap import MojmapParser
from parsers.mcp import MCPParser
from parsers.Yarn import YarnParser
from utils.mapping_utils import is_placeholder, readable_name, hint_for_entry


class MappingGitHub:
    def __init__(self):
        self.cache = {}
        self.cache_file = ".cache"
        self._init_db() # init sqlite cache

    def _init_db(self):
        conn = sqlite3.connect(self.cache_file)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, data BLOB)")
        conn.commit()
        conn.close()

    def load_cache(self, mapping_type, version): # fetch cached mappings
        key = f"{mapping_type}_{version}"
        try:
            conn = sqlite3.connect(self.cache_file)
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM cache WHERE key = ?", (key,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return pickle.loads(zlib.decompress(row[0]))
        except Exception:
            pass
        return None

    def save_cache(self, mapping_type, version, data):
        ## this faster now
        key = f"{mapping_type}_{version}"
        try:
            compressed = zlib.compress(pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL))
            conn = sqlite3.connect(self.cache_file)
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO cache (key, data) VALUES (?, ?)", (key, compressed))
            conn.commit()
            conn.close()
        except Exception:
            pass

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

    def download_url(self, url, description, progress_callback=None):
        if not progress_callback:
            r = requests.get(url)
            return r.text if r.status_code == 200 else None

        try:
            r = requests.get(url, stream=True)
            if r.status_code != 200:
                return None

            total = r.headers.get("content-length")
            chunks = []

            if total is None:
                progress_callback(description, -1)
                for chunk in r.iter_content(chunk_size=8192):
                    if progress_callback(description, -2):
                        return None
                    chunks.append(chunk)
            else:
                total = int(total)
                downloaded = 0
                for chunk in r.iter_content(chunk_size=8192):
                    if progress_callback(description, -2):
                        return None
                    downloaded += len(chunk)
                    percent = int(100 * downloaded / total)
                    progress_callback(description, percent)
                    chunks.append(chunk)

            content = b"".join(chunks)
            try:
                return content.decode("utf-8")
            except UnicodeDecodeError:
                return content
        except Exception:
            return None

    def fetch_version_manifest(self, progress_callback=None):
        url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
        raw = self.download_url(url, "downloading version manifest..", progress_callback)
        return json.loads(raw) if raw else None

    def get_version_json(self, version, progress_callback=None):
        manifest = self.fetch_version_manifest(progress_callback)
        if not manifest:
            return None

        for v in manifest["versions"]:
            if v["id"] == version:
                raw = self.download_url(v["url"], "downloading version info..", progress_callback)
                return json.loads(raw) if raw else None

        return None

    def fetch_mojmap(self, version, progress_callback=None):
        data = self.get_version_json(version, progress_callback)
        if not data:
            return None

        downloads = data.get("downloads", {})
        mappings = downloads.get("client_mappings") or downloads.get("server_mappings")
        if not mappings:
            return None

        return self.download_url(mappings["url"], "downloading mappings..", progress_callback)

    def fetch_mcp(self, version, progress_callback=None):
        url = f"https://raw.githubusercontent.com/MinecraftForge/MCPConfig/master/versions/{version}/joined.srg"
        return self.download_url(url, "downloading mappings..", progress_callback)

    def _normalize_yarn_version(self, version, progress_callback=None):
        if "+build." in version:
            return version

        url = f"https://meta.fabricmc.net/v2/versions/yarn/{version}"
        raw = self.download_url(url, "downloading version info..", progress_callback)
        if not raw:
            return None

        versions = json.loads(raw)
        if isinstance(versions, dict):
            versions = [versions]
        if not versions:
            return None

        versions.sort(key=lambda item: (item.get("stable", False), item.get("build", 0)), reverse=True)
        return versions[0].get("version")

    def fetch_yarn(self, version, progress_callback=None):
        yarn_version = self._normalize_yarn_version(version, progress_callback)
        if not yarn_version:
            return None

        url = f"https://maven.fabricmc.net/net/fabricmc/yarn/{yarn_version}/yarn-{yarn_version}.jar"
        raw = self.download_url(url, "downloading mappings..", progress_callback)
        if not raw or not isinstance(raw, bytes):
            return None

        with io.BytesIO(raw) as jar_data:
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

    def get_index(self, mapping_type, version, progress_callback=None):
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
            raw = self.fetch_mojmap(version, progress_callback)
            if not raw:
                return None
            index = MojmapParser().parse(raw)

        elif mapping_type == "mcp":
            if not self.is_mcp_version_allowed(version):
                return {"_invalid": True, "reason": "MCP only supports <= 1.12.x"}
            raw = self.fetch_mcp(version, progress_callback)
            if not raw:
                return None
            index = MCPParser().parse(raw)

        elif mapping_type == "yarn":
            raw = self.fetch_yarn(version, progress_callback)
            if not raw:
                return None
            index = YarnParser().parse(raw)

        else:
            return None

        self.cache[key] = index
        self.save_cache(mapping_type, version, index)
        return index

    def search(self, query, mapping_type, version, progress_callback=None):
        if mapping_type == "obfuscated":
            return self._search_obfuscated(query, version, progress_callback)

        index = self.get_index(mapping_type, version, progress_callback)
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

    def _search_obfuscated(self, query, version, progress_callback=None):
        for mapping_type in ["yarn", "mojmap", "mcp"]:
            if progress_callback and progress_callback("", -2):
                return {"error": "Search cancelled"}
            index = self.get_index(mapping_type, version, progress_callback)
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
