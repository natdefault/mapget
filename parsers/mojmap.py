import re

# updated this one too cuz it was bad

class MojmapParser:
    CLASS_RE = re.compile(r"^(?P<named>.+) -> (?P<obf>.+):$")

    METHOD_RE = re.compile(
        r"^(?:\d+:\d+:)?(?P<return>\S+)\s+(?P<name>\S+)\((?P<params>.*)\)(?::\d+:\d+)? -> (?P<obf>\S+)$"
    )

    FIELD_RE = re.compile(
        r"^(?P<type>\S+)\s+(?P<name>\S+) -> (?P<obf>\S+)$"
    )

    def parse(self, text):
        index = {}
        current_class = None

        for raw_line in text.splitlines():
            line = raw_line.rstrip()

            if not line.strip():
                continue

            if line.strip().startswith("#"):
                continue

            if not line.startswith("    "):
                match = self.CLASS_RE.match(line.strip())

                if not match:
                    continue

                named = match.group("named").replace("/", ".")
                obf = match.group("obf").replace("/", ".")

                current_class = named

                entry = {
                    "type": "class",
                    "named": named,
                    "obf": obf,
                    "path": named,
                }

                index[named] = entry
                index[obf] = entry

                continue

            if current_class is None:
                continue

            member = line.strip()

            method_match = self.METHOD_RE.match(member)

            if method_match:
                return_type = method_match.group("return")
                method_name = method_match.group("name")
                params = method_match.group("params")
                obf = method_match.group("obf")

                descriptor = f"{return_type}({params})"

                path = f"{current_class}.{method_name}"

                entry = {
                    "type": "method",
                    "named": method_name,
                    "obf": obf,
                    "class": current_class,
                    "descriptor": descriptor,
                    "path": path,
                }

                index[obf] = entry
                index[path] = entry

                continue

            field_match = self.FIELD_RE.match(member)

            if field_match:
                field_type = field_match.group("type")
                field_name = field_match.group("name")
                obf = field_match.group("obf")

                path = f"{current_class}.{field_name}"

                entry = {
                    "type": "field",
                    "named": field_name,
                    "obf": obf,
                    "class": current_class,
                    "descriptor": field_type,
                    "path": path,
                }

                index[obf] = entry
                index[path] = entry

        return index