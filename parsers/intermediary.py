class IntermediaryParser:
    def parse(self, text):
        index = {}

        classes = {}

        for raw_line in text.splitlines():
            line = raw_line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            parts = line.split("\t")

            if len(parts) <= 1:
                parts = line.split()

            kind = parts[0]

            if kind == "CLASS" and len(parts) >= 4:
                official = parts[1].replace("/", ".")
                intermediary = parts[2].replace("/", ".")
                named = parts[3].replace("/", ".")

                entry = {
                    "type": "class",
                    "official": official,
                    "intermediary": intermediary,
                    "named": named,
                    "path": intermediary,
                    "source_mapping": "intermediary",
                }

                index[official] = entry
                index[intermediary] = entry
                index[named] = entry

                classes[official] = entry
                classes[intermediary] = entry
                classes[named] = entry

            elif kind == "FIELD" and len(parts) >= 6:
                owner = parts[1].replace("/", ".")
                descriptor = parts[2]

                official = parts[3]
                intermediary = parts[4]
                named = parts[5]

                owner_name = classes.get(owner, {}).get("intermediary", owner)

                path = f"{owner_name}.{intermediary}"

                entry = {
                    "type": "field",
                    "official": official,
                    "intermediary": intermediary,
                    "named": named,
                    "class": owner_name,
                    "descriptor": descriptor,
                    "path": path,
                    "source_mapping": "intermediary",
                }

                index[official] = entry
                index[intermediary] = entry
                index[path] = entry

            elif kind == "METHOD" and len(parts) >= 6:
                owner = parts[1].replace("/", ".")
                descriptor = parts[2]

                official = parts[3]
                intermediary = parts[4]
                named = parts[5]

                owner_name = classes.get(owner, {}).get("intermediary", owner)

                path = f"{owner_name}.{intermediary}"

                entry = {
                    "type": "method",
                    "official": official,
                    "intermediary": intermediary,
                    "named": named,
                    "class": owner_name,
                    "descriptor": descriptor,
                    "path": path,
                    "source_mapping": "intermediary",
                }

                index[official] = entry
                index[intermediary] = entry
                index[path] = entry

        return index