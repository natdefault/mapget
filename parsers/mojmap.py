import re


class MojmapParser:
    CLASS_RE = re.compile(r"^(?P<named>.+) -> (?P<obf>.+):$")

    def parse(self, text):
        index = {}
        current_class = None
        current_class_obf = None

        for raw_line in text.splitlines():
            line = raw_line.rstrip("\n")
            if not line.strip() or line.strip().startswith("#"):
                continue

            if not line.startswith("    "):
                match = self.CLASS_RE.match(line.strip())
                if not match:
                    continue

                current_class = match.group("named")
                current_class_obf = match.group("obf")
                class_entry = {
                    "named": current_class,
                    "obf": current_class_obf,
                    "type": "class",
                    "path": current_class,
                }
                index[current_class] = class_entry
                index[current_class_obf] = class_entry
                continue

            if current_class is None:
                continue

            member_line = line.strip()
            if " -> " not in member_line:
                continue

            left, obf = [part.strip() for part in member_line.split("->", 1)]
            parts = left.split()
            if len(parts) < 2:
                continue

            if "(" in parts[-1] or "(" in parts[0]:
                member_type = "method"
                descriptor = parts[0]
                member_name = parts[1]
            else:
                member_type = "field"
                descriptor = parts[0]
                member_name = parts[1]

            path = f"{current_class}.{member_name}"
            entry = {
                "named": member_name,
                "obf": obf,
                "type": member_type,
                "class": current_class,
                "descriptor": descriptor,
                "path": path,
            }

            index[member_name] = entry
            index[obf] = entry

        return index
