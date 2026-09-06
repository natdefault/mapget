import os
import platform
import sys


def data_dir():
    if os.name == "nt":
        root = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    else:
        root = os.environ.get("XDG_DATA_HOME") or os.path.join(
            os.path.expanduser("~"), ".local", "share"
        )
    d = os.path.join(root, "mapget")
    try:
        os.makedirs(d, exist_ok=True)
    except OSError:
        pass
    return d


def cache_db():
    return os.path.join(data_dir(), "cache.db")


def cfg_db():
    return os.path.join(data_dir(), "mgcfg.db")


def plat_tag(os_tag=None):
    if os_tag is None:
        p = sys.platform
        if p.startswith("win"):
            os_tag = "windows"
        elif p.startswith("linux"):
            os_tag = "linux"
        elif p == "darwin":
            os_tag = "macos"
        else:
            os_tag = p
    mach = platform.machine().lower()
    if mach in ("amd64", "x64"):
        mach = "x86_64"
    elif mach in ("arm64",):
        mach = "aarch64"
    return f"{os_tag}-{mach}"
