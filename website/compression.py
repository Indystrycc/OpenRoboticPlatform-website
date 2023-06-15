import gzip
import shutil
from pathlib import Path


def compress_uploads(part_id: int, user_id: int):
    # Don't bother with images and 3MF. 3MF are already zip files (although may not be compressed)
    SUPPORTED_EXTENSIONS = (".stl", ".step")
    uploads_path = Path("website/static/uploads/files")
    for path in uploads_path.glob(
        f"part_{user_id}_{part_id}_*[{','.join(SUPPORTED_EXTENSIONS)}]"
    ):
        with open(path, "rb") as in_file:
            with gzip.open(path.with_suffix(path.suffix + ".gz"), "wb") as out_file:
                shutil.copyfileobj(in_file, out_file)