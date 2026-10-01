"""Build the self-contained web demo from its editable template and HD layers."""

import base64
import json
from pathlib import Path
import re

SOURCE = Path(__file__).resolve().parent
REPO = SOURCE.parents[1]


def prepare_template(native_page):
    """Allow the original pet-export workflow to refresh the same web template."""
    pattern = r"background-image:url\('data:image/png;base64,[A-Za-z0-9+/=]+'\);background-size:1536px 2288px;"
    page, count = re.subn(pattern, 'display:block;', native_page)
    assert count == 1, 'Expected the native preview sprite background'
    old = '<div class="sprite" id="sprite" role="img" aria-label="Prismo, a black cartoon triangle with tiny white and rainbow oval hands"></div>'
    new = '<canvas class="sprite" id="sprite" width="576" height="624" role="img" aria-label="Prismo, a black cartoon triangle with tiny white and rainbow oval hands"></canvas>'
    assert page.count(old) == 1
    page = page.replace(old, new)
    old = "function show(r,c){sprite.style.backgroundPosition=`${-192*c}px ${-208*r}px`}"
    new = "const prismoRenderer=createPrismoRenderer(sprite,prismoSources,prismoPoses);prismoRenderer.ready.catch(()=>{caption.textContent='Prismo could not load. Please refresh.'});function show(r,c){prismoRenderer.show(r,c)}"
    assert page.count(old) == 1
    page = page.replace(old, new)
    return page.replace('<script>', '<script>\n__PRISMO_RENDERER__\nconst prismoSources=__PRISMO_SOURCES__;\nconst prismoPoses=__PRISMO_POSES__;\n', 1)


def render(template):
    images = {path.stem.removeprefix('rig-'): 'data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode()
              for path in sorted((SOURCE/'layers').glob('*.png'))}
    assert len(images) == 5
    return (template.replace('__PRISMO_RENDERER__', (SOURCE/'renderer.js').read_text())
            .replace('__PRISMO_SOURCES__', json.dumps(images, separators=(',', ':')))
            .replace('__PRISMO_POSES__', (SOURCE/'poses.json').read_text().strip()))


if __name__ == '__main__':
    page = render((SOURCE/'template.html').read_text())
    for path in [REPO/'docs/index.html', REPO/'preview.html']:
        path.write_text(page)
    print(f'Rebuilt the HD web demo ({len(page.encode()):,} bytes).')
