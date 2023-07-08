import os
import re
import string
from pathlib import Path

import requests

FA_VERSION = "6.4.0"
BRAND_ICONS = ["github", "youtube", "instagram"]
SOLID_ICONS = [
    "file",
    "globe",
    "bars",
    "search",
    "question-circle",
    "circle-plus",
    "pen-to-square",
]

TARGET_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "../website/static/js/fa"
)
ICON_LINE = re.compile(
    r"^\s*(?P<name>\d+|(?:[a-z]\w*)|(?:\"[\w-]*\")):\s*\[\s*\d+,\s*\d+,\s*\[(?P<alt_names>(?:[\s\w\",-]+)?)\].*\],?$",
    flags=re.MULTILINE | re.ASCII,
)
EMPTY_LINES = re.compile(r"\n{2,}")


def download_file(file_base: str):
    url_base = f"https://github.com/FortAwesome/Font-Awesome/raw/{FA_VERSION}/js/{file_base}.min.js"
    r = requests.get(url_base)
    if r.status_code != 200:
        raise RuntimeError("Got unexpected response code", r)

    return r.text


def process_icon_set(data: str, icons: list[str]):
    def log_match(matchobj: re.Match):
        if matchobj.group("name").strip('"') in icons:
            return matchobj.group(0)

        alt_names = matchobj.group("alt_names")
        if not alt_names or type(alt_names) is not str:
            return ""

        alt_names = [x.strip(string.whitespace + '"') for x in alt_names.split(",")]
        for name in alt_names:
            if name in icons:
                return matchobj.group(0)
        return ""

    no_unnecessary = ICON_LINE.sub(log_match, data)
    return EMPTY_LINES.sub("\n", no_unnecessary)


if __name__ == "__main__":
    print("Downloading brands icon set")
    brands = download_file("brands")
    print("Filtering brand icons")
    brands = process_icon_set(brands, BRAND_ICONS)
    print("Downloading solid icon set")
    solid = download_file("solid")
    print("Filtering solid icons")
    solid = process_icon_set(solid, SOLID_ICONS)
    print("Downloading the Font Awesome script")
    script = download_file("fontawesome")

    print("Writing results")
    Path(TARGET_DIR).mkdir(parents=True, exist_ok=True)
    with open(
        os.path.join(TARGET_DIR, "brands.min.js"), "wt", newline="\n"
    ) as brands_file:
        brands_file.write(brands)
    with open(
        os.path.join(TARGET_DIR, "solid.min.js"), "wt", newline="\n"
    ) as solid_file:
        solid_file.write(solid)
    with open(
        os.path.join(TARGET_DIR, "fontawesome.min.js"), "wt", newline="\n"
    ) as fa_file:
        fa_file.write(script)
