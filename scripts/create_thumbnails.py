from mimetypes import guess_type
from pathlib import Path

from PIL import Image, UnidentifiedImageError

THUMBNAIL_EXTENSIONS = [".webp"]
THUMBNAIL_DIM = (548, 411)

project_root = Path(__file__).parents[1]
images_dir = project_root / "website" / "static" / "uploads" / "images"
thumbnails_dir = images_dir / "thumbs"


def generate_missing_thumbnails(source_file: Path) -> None:
    thumb_file = thumbnails_dir / source_file.name
    extensions = THUMBNAIL_EXTENSIONS.copy()
    mime = guess_type(source_file)[0]
    match mime:
        case "image/png":
            extensions.append(".png")
        case "image/jpeg":
            extensions.append(".jpg")
        case _:
            print(f"Unknown image format {mime}")
            return

    missing_thumbs = [
        thumb_file.with_suffix(ext)
        for ext in extensions
        if not thumb_file.with_suffix(ext).is_file()
    ]
    if not len(missing_thumbs):
        print("thumbnails already exist")
        return

    try:
        with Image.open(source_file) as img:
            thumb = make_thumbnail(img)
            for thumb_path in missing_thumbs:
                thumb.save(thumb_path)
                print(thumb_path.suffix, end=" ")
        print("")
    except UnidentifiedImageError as e:
        print(f"not a valid image:", e)


def check_all_thumbnails() -> None:
    if not thumbnails_dir.is_dir():
        print("Creating thumbnails directory")
        thumbnails_dir.mkdir(parents=True, exist_ok=True)
    for image in images_dir.glob("part*"):
        print(image, end=": ")
        generate_missing_thumbnails(image)


def make_thumbnail(
    img: Image.Image, size: tuple[int, int] = THUMBNAIL_DIM
) -> Image.Image:
    w, h = img.size
    x = min(w // 4, h // 3)
    cropped_w, cropped_h = 4 * x, 3 * x

    if cropped_w != w or cropped_h != h:
        offset_x, offset_y = 0, 0
        if cropped_w < w:
            offset_x = (w - cropped_w) // 2
        if cropped_h < h:
            offset_y = (h - cropped_h) // 2
        thumb = img.crop(
            (offset_x, offset_y, offset_x + cropped_w, offset_y + cropped_h)
        )
    else:
        thumb = img

    thumb.thumbnail(size, Image.Resampling.LANCZOS)
    return thumb


if __name__ == "__main__":
    check_all_thumbnails()
