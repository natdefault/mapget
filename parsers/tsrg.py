class TSRGParser:
    def parse(self, text):
        index = {}

        current_obf_class = None
        current_named_class = None

        for raw_line in text.splitlines():
            line = raw_line.rstrip()

            if not line.strip():
                continue

            if not line.startswith("\t") and not line.startswith("    "):
                parts = line.strip().split()

                if len(parts) < 2:
                    continue

                current_obf_class = parts[0].replace("/", ".")
                current_named_class = parts[1].replace("/", ".")

                entry = {
                    "type": "class",
                    "obfuscated": current_obf_class,
                    "deobfuscated": current_named_class,
                    "path": current_named_class,
                    "mapping": "tsrg",
                }

                index[current_obf_class] = entry
                index[current_named_class] = entry

                continue

            if current_named_class is None:
                continue

            parts = line.strip().split()

            if len(parts) == 2:
                obf_name = parts[0]
                named_name = parts[1]

                path = f"{current_named_class}.{named_name}"

                entry = {
                    "type": "field",
                    "obfuscated": obf_name,
                    "deobfuscated": named_name,
                    "class": current_named_class,
                    "path": path,
                    "mapping": "tsrg",
                }

                index[obf_name] = entry
                index[named_name] = entry
                index[path] = entry

            elif len(parts) >= 3:
                obf_name = parts[0]
                descriptor = parts[1]
                named_name = parts[2]

                path = f"{current_named_class}.{named_name}"

                entry = {
                    "type": "method",
                    "obfuscated": obf_name,
                    "deobfuscated": named_name,
                    "class": current_named_class,
                    "descriptor": descriptor,
                    "path": path,
                    "mapping": "tsrg",
                }

                index[obf_name] = entry
                index[named_name] = entry
                index[path] = entry

        return index