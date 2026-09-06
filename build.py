# mapget build tool

import os
import sys
import subprocess
from datetime import datetime

from utils.paths import plat_tag


def parse_args(argv):
    version = ""
    tgts = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--version" and i + 1 < len(argv):
            version = argv[i + 1]
            i += 2
            continue
        if arg in ("--win", "--windows", "win", "windows"):
            tgts.append("windows")
        elif arg in ("--linux", "linux"):
            tgts.append("linux")
        elif arg in ("--all", "all"):
            tgts.extend(["windows", "linux"])
        elif not arg.startswith("-") and not version:
            version = arg
        i += 1
    if not tgts:
        tgts = ["windows"] if os.name == "nt" else ["linux"]
    seen = []
    for t in tgts:
        if t not in seen:
            seen.append(t)
    return version, seen


def host_ok(tgt):
    if tgt == "windows":
        return os.name == "nt"
    return os.name != "nt"


def write_ver(version, build_date, tgt):
    tag = plat_tag(tgt)
    with open("version.py", "w", encoding="utf-8") as f:
        f.write(f'VERSION = "{version}"\n')
        f.write(f'BUILD_DATE = "{build_date}"\n')
        f.write(f'TARGET = "{tag}"\n')


def pyi_cmd(tgt):
    sep = ";" if tgt == "windows" else ":"
    icon = "assets/helpsheet.ico" if tgt == "windows" else "assets/helpsheet.png"
    return [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name=mapget",
        f"--icon={icon}",
        "--add-data",
        f"assets{sep}assets",
        "main.py"
    ]


def main():
    version, tgts = parse_args(sys.argv[1:])
    build_date = datetime.now().strftime("%m/%d/%Y")

    for tgt in tgts:
        if not host_ok(tgt):
            print(f"skip {tgt}: wrong host")
            continue
        write_ver(version, build_date, tgt)
        print(f"building {plat_tag(tgt)}")
        subprocess.run(pyi_cmd(tgt), check=True)


if __name__ == "__main__":
    main()
