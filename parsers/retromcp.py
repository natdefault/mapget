import csv
import io


class RetroMCPParser:
    def parse(self, text):
        index = {}

        reader = csv.reader(io.StringIO(text))

        for row in reader:
            if len(row) < 2:
                continue

            srg = row[0].strip()
            named = row[1].strip()

            if not srg:
                continue

            entry_type = "unknown"

            if srg.startswith("func_"):
                entry_type = "method"
            elif srg.startswith("field_"):
                entry_type = "field"

            entry = {
                "type": entry_type,
                "obfuscated": srg,
                "deobfuscated": named,
                "mapping": "retromcp",
            }

            index[srg] = entry
            index[named] = entry

        return index