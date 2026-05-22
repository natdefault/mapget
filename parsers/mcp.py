import re

#atp i dont know if this one worked but whatever bro

class MCPParser:
    def parse(self, text):
        index = {}

        for line in text.splitlines():
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split()

            if len(parts) < 3:
                continue

            srg = parts[0]
            obf = parts[1]
            named = parts[2]

            index[srg] = {
                "obf": obf,
                "named": named,
                "type": "mcp"
            }

        return index