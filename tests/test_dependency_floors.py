"""Keep runtime dependency floors above versions with known security fixes.

pip does not upgrade an already-installed dependency that still satisfies the
declared range, so a loose lower bound lets users keep running a vulnerable
version underneath FinMind.
"""

import pathlib
import re

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    import tomli as tomllib

PYPROJECT = pathlib.Path(__file__).resolve().parents[1] / "pyproject.toml"

# package -> minimum version that must be required on every Python version
SECURITY_FLOORS = {
    # Proxy-Authorization leak on redirect, verify=False session reuse,
    # .netrc credential leak to third-party hosts
    "requests": (2, 32, 4),
    # arbitrary code execution when reading untrusted IPC / Parquet data
    "pyarrow": (14, 0, 1),
    # HTTP parsing / request smuggling fixes
    "aiohttp": (3, 10, 11),
    # libxml2 / XML parsing fixes
    "lxml": (5, 0, 0),
    # arbitrary code execution via CLI arguments
    "tqdm": (4, 66, 3),
}

# package -> minimum version required on Python >= 3.10, where the newest
# security releases are installable (they dropped Python 3.8 / 3.9).
SECURITY_FLOORS_PY310 = {
    "aiohttp": (3, 14, 4),
    "pyarrow": (23, 0, 1),
}


def _lower_bound(requirement: str):
    match = re.search(r">=\s*([0-9]+(?:\.[0-9]+)*)", requirement)
    if not match:
        return None
    return tuple(int(part) for part in match.group(1).split("."))


def _dependencies():
    with PYPROJECT.open("rb") as f:
        deps = tomllib.load(f)["project"]["dependencies"]
    result = {}
    for dep in deps:
        name = re.split(r"[<>=!~;\[ ]", dep, maxsplit=1)[0].lower()
        result.setdefault(name, []).append(dep)
    return result


def test_security_floors():
    deps = _dependencies()
    for name, floor in SECURITY_FLOORS.items():
        assert name in deps, f"{name} missing from dependencies"
        for requirement in deps[name]:
            bound = _lower_bound(requirement)
            assert (
                bound is not None
            ), f"{name} has no lower bound: {requirement}"
            assert bound >= floor, f"{name} lower bound {bound} < {floor}"


def test_security_floors_py310():
    deps = _dependencies()
    for name, floor in SECURITY_FLOORS_PY310.items():
        modern = [
            requirement
            for requirement in deps[name]
            if "python_version >= '3.10'" in requirement
        ]
        assert modern, f"{name} has no Python >= 3.10 requirement"
        for requirement in modern:
            bound = _lower_bound(requirement)
            assert bound >= floor, f"{name} lower bound {bound} < {floor}"
