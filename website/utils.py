from typing import Mapping


def merge_arr(a: str | list[str], b: str | list[str]) -> str | list[str]:
    if a == "":
        return b
    if b == "":
        return a
    a = [a] if isinstance(a, str) else a
    return a + [b] if isinstance(b, str) else a + b


def extend_talisman_csp(
    base_csp: dict[str, str | list[str]], *extensions: Mapping[str, str | list[str]]
) -> dict[str, str | list[str]]:
    copy = base_csp.copy()
    for extension in extensions:
        for key, value in extension.items():
            if key not in copy:
                copy[key] = value
            else:
                copy[key] = merge_arr(copy[key], value)
    return copy
