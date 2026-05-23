class SRGParser:
    def parse(self, text):
        index = {}

        for raw_line in text.splitlines():
            line = raw_line.strip()

            if not line:
                continue

            if line.startswith("CL:"):
                parts = line.split()

                if len(parts) < 3:
                    continue

                obf = parts[1].replace("/", ".")
                srg = parts[2].replace("/", ".")

                entry = {
                    "type": "class",
                    "obfuscated": obf,
                    "deobfuscated": srg,
                    "path": srg,
                    "mapping": "srg",
                }

                index[obf] = entry
                index[srg] = entry

            elif line.startswith("FD:"):
                parts = line.split()

                if len(parts) < 3:
                    continue

                obf_path = parts[1].replace("/", ".")
                srg_path = parts[2].replace("/", ".")

                obf_class, obf_name = obf_path.rsplit(".", 1)
                srg_class, srg_name = srg_path.rsplit(".", 1)

                entry = {
                    "type": "field",
                    "obfuscated": obf_name,
                    "deobfuscated": srg_name,
                    "class": srg_class,
                    "path": srg_path,
                    "mapping": "srg",
                }

                index[obf_name] = entry
                index[srg_name] = entry
                index[srg_path] = entry

            elif line.startswith("MD:"):
                parts = line.split()

                if len(parts) < 5:
                    continue

                obf_path = parts[1].replace("/", ".")
                obf_desc = parts[2]

                srg_path = parts[3].replace("/", ".")
                srg_desc = parts[4]

                obf_class, obf_name = obf_path.rsplit(".", 1)
                srg_class, srg_name = srg_path.rsplit(".", 1)

                entry = {
                    "type": "method",
                    "obfuscated": obf_name,
                    "deobfuscated": srg_name,
                    "class": srg_class,
                    "descriptor": srg_desc,
                    "obf_descriptor": obf_desc,
                    "path": srg_path,
                    "mapping": "srg",
                }

                index[obf_name] = entry
                index[srg_name] = entry
                index[srg_path] = entry

        return index