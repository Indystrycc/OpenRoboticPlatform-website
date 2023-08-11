import os
from pathlib import Path

from PIL import Image
from werkzeug.datastructures import FileStorage

ImgSize = tuple[int, int]

# Warn on 32 MP images, raise an error on 64 MB
Image.MAX_IMAGE_PIXELS = 32_000_000


# Largest possible thumbnail size is 548 x 411 px
# Thumbnails have 4:3 aspect ratio
def prepare_thumbnail(img: Image.Image, size: ImgSize):
    w, h = img.size
    x = min(w // 4, h // 3)
    cropped_w, cropped_h = 4 * x, 3 * x

    thumb = img.copy()
    if cropped_w != w or cropped_h != h:
        offset_x, offset_y = 0, 0
        if cropped_w < w:
            offset_x = (w - cropped_w) // 2
        if cropped_h < h:
            offset_y = (h - cropped_h) // 2
        thumb = thumb.crop(
            (offset_x, offset_y, offset_x + cropped_w, offset_y + cropped_h)
        )

    thumb.thumbnail(size, Image.LANCZOS)
    return thumb


def create_thumbnails(
    img: Image.Image,
    dir: str | Path,
    filename: str,
    size: ImgSize = (548, 411),
    extensions: list[str] = [".webp"],
):
    thumb = prepare_thumbnail(img, size)
    dir = Path(dir)
    if not dir.is_dir():
        dir.mkdir(parents=True, exist_ok=True)

    basename, _ = os.path.splitext(filename)
    match img.format:
        case "PNG":
            extensions.append(".png")
        case "JPEG":
            extensions.append(".jpg")
        case _:
            raise RuntimeError(f"Unknown format {img.format}")
    for ext in extensions:
        fname = f"{basename}{ext}"
        dest = dir / fname
        thumb.save(dest)


def load_check_image(
    file: FileStorage, min_size: ImgSize = (548, 411), allowed_formats=("JPEG", "PNG")
):
    img = Image.open(file, formats=allowed_formats)

    w, h = img.size
    if w < min_size[0] or h < min_size[1]:
        raise ValueError(
            f"Image is too small. Expected at least {min_size[0]}x{min_size[1]} px, but the image is only {w}x{h} px."
        )

    return img
