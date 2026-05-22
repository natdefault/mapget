# we hate yarn!

class YarnParser:
    def parse(self, text):
        index = {}
        classes = {}

        for raw_line in text.splitlines():
            if not raw_line or raw_line.startswith("#"):
                continue

            parts = raw_line.split("\t")
            kind = parts[0]

            if kind == "CLASS" and len(parts) >= 4:
                official, intermediary, named = parts[1:4]
                intermediary = intermediary.replace("/", ".")
                named = named.replace("/", ".")

                entry = {
                    "type": "class",
                    "obf": official,
                    "intermediary": intermediary,
                    "named": named,
                    "path": named,
                }
                index[official] = entry
                index[intermediary] = entry
                index[named] = entry
                classes[official] = entry
                classes[intermediary] = entry
                classes[named] = entry

            elif kind == "FIELD" and len(parts) >= 6:
                owner, descriptor, official, intermediary, named = parts[1:6]
                owner_name = classes.get(owner, {}).get("named", owner)
                owner_name = owner_name.replace("/", ".")
                path = f"{owner_name}.{named}"

                entry = {
                    "type": "field",
                    "obf": official,
                    "intermediary": intermediary,
                    "named": named,
                    "class": owner_name,
                    "descriptor": descriptor,
                    "path": path,
                }
                index[official] = entry
                index[intermediary] = entry
                index[named] = entry

            elif kind == "METHOD" and len(parts) >= 6:
                owner, descriptor, official, intermediary, named = parts[1:6]
                owner_name = classes.get(owner, {}).get("named", owner)
                owner_name = owner_name.replace("/", ".")
                path = f"{owner_name}.{named}"

                entry = {
                    "type": "method",
                    "obf": official,
                    "intermediary": intermediary,
                    "named": named,
                    "class": owner_name,
                    "descriptor": descriptor,
                    "path": path,
                }
                index[official] = entry
                index[intermediary] = entry
                index[named] = entry

        return index
