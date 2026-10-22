"""Build a Petdex atlas whose first six frames also loop correctly in Hermes."""

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
FRAME_WIDTH, FRAME_HEIGHT = 192, 208
COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6]


def build():
    sheet = Image.open(REPO / 'hermes/prismo/spritesheet.png').convert('RGBA')
    assert sheet.size == (1536, 1872)
    # Hermes plays six frames in these rows. Petdex plays eight.
    # Hold the complete loop's last pose in the two additional Petdex cells.
    for row in (1, 2, 5):
        last = sheet.crop((5 * FRAME_WIDTH, row * FRAME_HEIGHT,
                           6 * FRAME_WIDTH, (row + 1) * FRAME_HEIGHT))
        for column in (6, 7):
            sheet.paste(last, (column * FRAME_WIDTH, row * FRAME_HEIGHT))
    for row, count in enumerate(COUNTS):
        for column in range(8):
            cell = sheet.crop((column * FRAME_WIDTH, row * FRAME_HEIGHT,
                               (column + 1) * FRAME_WIDTH, (row + 1) * FRAME_HEIGHT))
            assert bool(cell.getchannel('A').getbbox()) == (column < count)
    sheet.save(ROOT / 'spritesheet.png', optimize=True)
    metadata = {
        'id': 'prismo',
        'displayName': 'Prismo',
        'description': "Your friend from the dark side. A floating prism with white and rainbow hands. Inspired by Pink Floyd's The Dark Side of the Moon.",
        'spritesheetPath': 'spritesheet.png',
        'spriteVersionNumber': 1,
        'author': 'Audiofool',
        'source': 'https://github.com/Audiofool934/prismo',
        'license': 'CC-BY-4.0',
        'licenseUrl': 'https://creativecommons.org/licenses/by/4.0/',
    }
    (ROOT / 'pet.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print('Built Petdex v1 atlas: 57 populated cells; Hermes loops preserved.')


if __name__ == '__main__':
    build()
