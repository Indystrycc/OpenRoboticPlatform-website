import os
import re
import string
import sys
import warnings
from pathlib import Path
from typing import Literal, TypedDict

dirname = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(dirname, "..", "scripts"))
from create_fa_set import BRAND_ICONS, ICON_LINE, SOLID_ICONS

# No, I'm definitely not parsing HTML using regular expressions
# https://stackoverflow.com/a/1732454
HTML_CLASS = re.compile(r"class=\"([^\"]+)\"", flags=re.IGNORECASE)
JS_CLASSLIST = re.compile(
    r"\.\s*classList\s*\.\s*add\s*\(\s*(?P<classes>(?P<q>\"|')[\w-]*(?P=q)\s*(?:,\s*(?P<q2>\"|')[\w-]*(?P=q2))*)\s*\)"
)
JS_CLASSNAME = re.compile(
    r"\.\s*className\s*=\s*(?P<q>\"|')(?P<classes>[\w\s-]*)(?P=q)"
)
IGNORED_FA_CLASSES = set(
    [
        "fa-1x",
        "fa-2x",
        "fa-3x",
        "fa-4x",
        "fa-5x",
        "fa-6x",
        "fa-7x",
        "fa-8x",
        "fa-9x",
        "fa-10x",
        "fa-2xs",
        "fa-xs",
        "fa-sm",
        "fa-lg",
        "fa-xl",
        "fa-2xl",
        "fa-fw",
        "fa-ul",
        "fa-li",
        "fa-rotate-90",
        "fa-rotate-180",
        "fa-rotate-270",
        "fa-flip-horizontal",
        "fa-flip-vertical",
        "fa-flip-both",
        "fa-rotate-by",
        "fa-beat",
        "fa-fade",
        "fa-beat-fade",
        "fa-bounce",
        "fa-flip",
        "fa-shake",
        "fa-spin",
        "fa-spin-pulse",
        "fa-spin-reverse",
        "fa-border",
        "fa-pull-right",
        "fa-pull-left",
        "fa-stack",
        "fa-stack-1x",
        "fa-stack-2x",
        "fa-inverse",
        "fa-layers",
        "fa-layers-text",
        "fa-layers-counter",
        "fa-layers-bottom-left",
        "fa-layers-bottom-right",
        "fa-layers-top-left",
        "fa-layers-top-right",
        "fa-sr-only",
        "fa-sr-only-focusable",
    ]
)


class Icons(TypedDict):
    """Found icons grouped by icon set."""

    brands: set[str]
    solid: set[str]
    regular: set[str]


IconStyle = Literal["solid", "brands", "regular"] | None

project_path = Path(dirname, "../website/")
fa_path = project_path / "static/fa"


def process_single_class_list(
    classes: list[str], file_path: str | os.PathLike
) -> tuple[list[str], set[str], IconStyle]:
    errors: list[str] = []
    icons = set()
    style: IconStyle = None
    current_icon = None

    for c in classes:
        detected_style: IconStyle = None
        if c == "fa" or c == "fas" or c == "fa-solid":
            detected_style = "solid"
        elif c == "fab" or c == "fa-brands":
            detected_style = "brands"
        elif c == "far" or c == "fa-regular":
            detected_style = "regular"
            errors.append(
                f"{file_path}: Found a FA icon using the regular style, but regular icons are not included"
            )
        if detected_style:
            if style:
                errors.append(
                    f"{file_path}: Multiple styles declared for a single icon"
                )
            style = detected_style
            continue
        if c.startswith("fa-") and c not in IGNORED_FA_CLASSES:
            icon = c[3:]
            if not icon:
                errors.append(
                    f'{file_path}: "fa-" prefix found with nothing that follows it'
                )
                continue
            if current_icon:
                errors.append(
                    f'{file_path}: Multiple icons declared in a single class attribute - "{current_icon}" and "{icon}"'
                )
            current_icon = icon
            icons.add(icon)

    return errors, icons, style


def find_all_html_icons() -> tuple[list[str], Icons]:
    pages = project_path.glob("**/*.html")

    errors: list[str] = []
    icons: Icons = {"brands": set(), "regular": set(), "solid": set()}

    for page_path in pages:
        if not page_path.is_file():
            continue
        with open(page_path, "rt") as page_file:
            page = page_file.read()
            for match in HTML_CLASS.finditer(page):
                classes = match.group(1)
                if not classes:
                    warnings.warn(f"{page_path}: Empty class attribute found")
                classes = [x.strip() for x in classes.split(" ")]
                c_errors, c_icons, style = process_single_class_list(classes, page_path)
                errors.extend(c_errors)
                if style:
                    icons[style].update(c_icons)

    return errors, icons


def find_all_js_icons() -> tuple[list[str], Icons]:
    pages = project_path.glob("**/*.js")

    errors: list[str] = []
    icons: Icons = {"brands": set(), "regular": set(), "solid": set()}

    for script_path in pages:
        if fa_path in script_path.parents or not script_path.is_file():
            continue
        with open(script_path, "rt") as page_file:
            page = page_file.read()
            for match in JS_CLASSLIST.finditer(page):
                classes = match.group("classes")
                if not classes:
                    warnings.warn(f"{script_path}: Empty classList.add() found")
                classes = [x.strip()[1:-1] for x in classes.split(",")]
                c_errors, c_icons, style = process_single_class_list(
                    classes, script_path
                )
                errors.extend(c_errors)
                if style:
                    icons[style].update(c_icons)
            for match in JS_CLASSNAME.finditer(page):
                classes = match.group("classes")
                classes = [x.strip() for x in classes.split(" ")]
                c_errors, c_icons, style = process_single_class_list(
                    classes, script_path
                )
                errors.extend(c_errors)
                if style:
                    icons[style].update(c_icons)

    return errors, icons


def find_all_icons() -> tuple[list[str], Icons]:
    errors, icons = find_all_html_icons()
    js_errors, js_icons = find_all_js_icons()
    errors.extend(js_errors)
    icons["brands"].update(js_icons["brands"])
    icons["solid"].update(js_icons["solid"])
    icons["regular"].update(js_icons["regular"])
    return errors, icons


def check_in_create_script(icons: Icons):
    errors: list[str] = []
    not_found_icons: Icons = {"brands": set(), "regular": set(), "solid": set()}
    found_icons: Icons = {"brands": set(), "regular": set(), "solid": set()}
    for icon in icons["brands"]:
        if icon not in BRAND_ICONS:
            errors.append(f'Brand icon "{icon}" is not listed in BRAND_ICONS')
            not_found_icons["brands"].add(icon)
        else:
            found_icons["brands"].add(icon)
    for icon in icons["solid"]:
        if icon not in SOLID_ICONS:
            errors.append(f'Solid icon "{icon}" is not listed in SOLID_ICONS')
            not_found_icons["solid"].add(icon)
        else:
            found_icons["solid"].add(icon)

    unnecessary_brands_icons = set(BRAND_ICONS).difference(found_icons["brands"])
    unnecessary_solid_icons = set(SOLID_ICONS).difference(found_icons["solid"])
    unnecessary_icons: Icons = {
        "brands": unnecessary_brands_icons,
        "regular": set(),
        "solid": unnecessary_solid_icons,
    }
    for icon in unnecessary_brands_icons:
        errors.append(f'Unused brand icon "{icon}" found in BRAND_ICONS')
    for icon in unnecessary_solid_icons:
        errors.append(f'Unused solid icon "{icon}" found in SOLID_ICONS')

    return errors, not_found_icons, unnecessary_icons


def all_names_from_js(script: str):
    names: list[str] = []
    for match in ICON_LINE.finditer(script):
        name = match.group("name").strip('"')
        names.append(name)
        alt_names = match.group("alt_names")
        if type(alt_names) is str:
            alt_names = [x.strip(string.whitespace + '"') for x in alt_names.split(",")]
            names.extend(alt_names)
    return names


def check_minimized_fa_scripts(icons: Icons):
    errors: list[str] = []
    not_found_icons: Icons = {"brands": set(), "regular": set(), "solid": set()}
    with open(fa_path / "brands.min.js", "rt") as brands_file:
        brands_data = brands_file.read()
        brands = all_names_from_js(brands_data)
        for icon in icons["brands"]:
            if icon not in brands:
                errors.append(
                    f'Brand icon "{icon}" is not listed in the FontAwesome brands.min.js file. Make sure that it\'s in BRAND_ICONS and run create_fa_set.py'
                )
                not_found_icons["brands"].add(icon)
    with open(fa_path / "solid.min.js", "rt") as solid_file:
        solid_data = solid_file.read()
        solid = all_names_from_js(solid_data)
        for icon in icons["solid"]:
            if icon not in solid:
                errors.append(
                    f'Solid icon "{icon}" is not listed in the FontAwesome solid.min.js file. Make sure that it\'s in SOLID_ICONS and run create_fa_set.py'
                )
                not_found_icons["solid"].add(icon)

    return errors, not_found_icons


def test_icons():
    errors, icons = find_all_icons()
    e, nf_py_script, nu_py_script = check_in_create_script(icons)
    errors.extend(e)
    e, nf_js_min = check_minimized_fa_scripts(icons)
    errors.extend(e)
    return errors, nf_py_script, nf_js_min, nu_py_script


if __name__ == "__main__":
    errors, nf_py_script, nf_js_min, nu_py_script = test_icons()
    for error in errors:
        print(error, file=sys.stderr)

    missing_script = len(nf_py_script["brands"]) + len(nf_py_script["solid"])
    missing_generated = len(nf_js_min["brands"]) + len(nf_js_min["solid"])
    unnecessary_script = len(nu_py_script["brands"]) + len(nu_py_script["solid"])

    if unnecessary_script:
        print(
            "Remove unused icons from scripts/create_fa_set.py and run it to regenerate minimized icon sets",
            file=sys.stderr,
        )
    if missing_script:
        print(
            "Add the missing icons to scripts/create_fa_set.py and run it to generate minimized icon sets",
            file=sys.stderr,
        )
    if unnecessary_script or missing_script:
        exit(1)
    if missing_generated:
        print(
            "Did you forget to run scripts/create_fa_set.py? It contains all necessary icons, but the minimized icon sets are outdated.",
            file=sys.stderr,
        )
        exit(2)

    # Other errors were generated (regular icons or invalid syntax)
    if len(errors):
        exit(3)

    print("Success!")
    exit(0)
