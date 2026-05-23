# mapget build tool

import os
import sys
import subprocess
from datetime import datetime


def main():
    version = ""
    args = sys.argv[1:]

    if len(args) > 0:
        if args[0] == "--version" and len(args) > 1:
            version = args[1]
        elif not args[0].startswith("-"):
            version = args[0]
    # write release
    build_date = datetime.now().strftime("%m/%d/%Y")
    with open("version.py", "w", encoding="utf-8") as f:
        f.write(f'VERSION = "{version}"\n')
        f.write(f'BUILD_DATE = "{build_date}"\n')

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name=mapget",
        "--icon=assets/helpsheet.ico",
        "--add-data",
        f"assets{';' if os.name == 'nt' else ':'}assets",
        "main.py"
    ]

    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
