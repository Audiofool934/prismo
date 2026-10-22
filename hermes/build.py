"""Build the Hermes package from Prismo's approved native sprite sheet.

Run with Python 3 and Pillow: python3 hermes/build.py.
No frame is resized, redrawn, or blended.
"""

import hashlib
import json
from pathlib import Path
import zipfile

from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
WIDTH, HEIGHT = 192, 208
STATES = [
    "idle", "running-right", "running-left", "waving", "jumping",
    "failed", "waiting", "running", "review",
]
# Sample the whole eight-frame loop, including its first and last poses.
# Keep shorter animations intact so Hermes can trim transparent padding.
SOURCE_COLUMNS = [
    [0, 1, 2, 3, 4, 5],
    [0, 1, 3, 4, 6, 7],
    [0, 1, 3, 4, 6, 7],
    [0, 1, 2, 3],
    [0, 1, 2, 3, 4],
    [0, 1, 3, 4, 5, 7],
    [0, 1, 2, 3, 4, 5],
    [0, 1, 2, 3, 4, 5],
    [0, 1, 2, 3, 4, 5],
]


def build():
    source = REPO / "spritesheet.png"
    image = Image.open(source).convert("RGBA")
    if image.size != (1536, 2288):
        raise ValueError("Expected the approved 8-column v2 sheet")
    sheet = Image.new("RGBA", (WIDTH * 8, HEIGHT * 9))
    for row, columns in enumerate(SOURCE_COLUMNS):
        for target, column in enumerate(columns):
            frame = image.crop((column * WIDTH, row * HEIGHT,
                                (column + 1) * WIDTH, (row + 1) * HEIGHT))
            if frame.getchannel("A").getextrema()[1] <= 8:
                raise ValueError(f"Blank source frame: {row}, {column}")
            sheet.paste(frame, (target * WIDTH, row * HEIGHT))
    package = HERE / "prismo"
    package.mkdir(exist_ok=True)
    sheet.save(package / "spritesheet.png", optimize=True)
    metadata = {
        "id": "prismo",
        "displayName": "Prismo",
        "description": "Your friend from the dark side. A floating prism with white and rainbow hands.",
        "spritesheetPath": "spritesheet.png",
    }
    (package / "pet.json").write_text(json.dumps(metadata, indent=2) + "\n")
    provenance = {
        "source": "../spritesheet.png",
        "sourceSha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "frameWidth": WIDTH, "frameHeight": HEIGHT,
        "columns": 8, "rows": 9,
        "framesPerRow": [len(c) for c in SOURCE_COLUMNS],
        "states": STATES, "sourceColumnsByRow": SOURCE_COLUMNS,
        "loopMs": 1100,
        "timing": "Hermes controls playback timing; each state loops in 1100 ms.",
    }
    (HERE / "animation.json").write_text(json.dumps(provenance, indent=2) + "\n")
    # Fixed timestamps and permissions make the download reproducible.
    with zipfile.ZipFile(HERE / "prismo-hermes.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for name in ("pet.json", "spritesheet.png"):
            path = package / name
            info = zipfile.ZipInfo(f"prismo/{path.name}", (2026, 10, 22, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    print(f"Built Hermes package: {sum(provenance['framesPerRow'])} frames across nine rows.")


if __name__ == "__main__":
    build()
