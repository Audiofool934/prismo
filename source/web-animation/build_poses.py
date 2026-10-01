"""Fit the approved pet's poses, then render its original high-resolution layers.

The small atlas supplies motion only. All displayed character pixels come from
the high-resolution artwork already used in the Prismo film.
"""

import base64
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage, optimize


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
QA = HERE / 'qa'
ASSETS = HERE / 'layers'
COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]
NAMES = ['body', 'left-hand', 'right-hand', 'eye-1', 'eye-2']
LAYERS = {name: Image.open(ASSETS / f'rig-{name}.png').convert('RGBA') for name in NAMES}


def components(mask):
    labels, count = ndimage.label(mask)
    return sorted([labels == i for i in range(1, count+1)], key=np.count_nonzero, reverse=True)


def bbox(mask):
    yy, xx = np.where(mask)
    return np.array([xx.min(), yy.min(), xx.max()+1, yy.max()+1], float)


def outline(mask, maximum=240):
    yy, xx = np.where(mask & ~ndimage.binary_erosion(mask))
    points = np.column_stack([xx, yy]).astype(float)
    return points[np.linspace(0, len(points)-1, min(maximum, len(points))).astype(int)]


def distance(mask):
    return ndimage.distance_transform_edt(~mask) - ndimage.distance_transform_edt(mask)


def matrix(parameters, source_box):
    cx, cy, width, height, angle, shear = parameters
    co, si = math.cos(angle), math.sin(angle)
    source_size = source_box[2:] - source_box[:2]
    center = (source_box[:2] + source_box[2:] - 1) / 2
    linear = np.array([[co, -si], [si, co]]) @ np.array([[width, shear*height], [0, height]]) @ np.diag(1/source_size)
    translation = np.array([cx, cy]) - linear @ center
    return linear, translation


def fit(source, target, name):
    sm = np.asarray(source.getchannel('A')) > 128
    tm = target > .5
    sb, tb = bbox(sm), bbox(tm)
    sp, tp = outline(sm), outline(tm)
    sd, td = distance(sm), distance(tm)
    center = (tb[:2] + tb[2:] - 1) / 2
    size = tb[2:] - tb[:2]
    start = [*center, *size, 0, 0]

    def residual(p):
        linear, translation = matrix(p, sb)
        mapped = sp @ linear.T + translation
        a = ndimage.map_coordinates(td, mapped[:, ::-1].T, order=1, mode='constant', cval=30)
        inverse = (tp-translation) @ np.linalg.inv(linear).T
        b = ndimage.map_coordinates(sd, inverse[:, ::-1].T, order=1, mode='constant', cval=150) * math.sqrt(np.linalg.det(linear))
        return np.concatenate([a, b, [p[5]*3]])

    result = optimize.least_squares(residual, start, bounds=(
        [center[0]-12, center[1]-12, size[0]*.55, size[1]*.55, -.65, -.25],
        [center[0]+12, center[1]+12, size[0]*1.5, size[1]*1.5, .65, .25]),
        max_nfev=90, ftol=1e-6, xtol=1e-6, gtol=1e-6)
    linear, translation = matrix(result.x, sb)
    affine = [linear[0,0], linear[1,0], linear[0,1], linear[1,1], *translation]
    return [round(float(x), 7) for x in affine], float(np.sqrt(np.mean(residual(result.x)**2)))


def cell_parts(frame):
    rgba = np.asarray(frame)
    alpha = rgba[..., 3] / 255
    masks = components(alpha > .06)[:3]
    assert len(masks) == 3
    body = masks[0]
    hands = sorted(masks[1:], key=lambda m: bbox(m)[0])
    rgb = rgba[..., :3].astype(float)
    white = ((rgb.min(axis=2) > 120) & (rgb.max(axis=2)-rgb.min(axis=2) < 45)
             & ndimage.binary_erosion(body, iterations=5))
    eyes = sorted(components(white)[:2], key=lambda m: bbox(m)[0])
    assert len(eyes) == 2
    return [alpha*m for m in [body, *hands]] + [np.minimum(rgb.min(axis=2)/255, alpha)*ndimage.binary_dilation(m) for m in eyes]


def paint(parts, factor=3):
    canvas = Image.new('RGBA', (192*factor, 208*factor))
    for part in parts:
        src = LAYERS[part['image']]
        if 'crop' in part:
            x, y, w, h = part['crop']
            src = src.crop((x, y, x+w, y+h))
        a,b,c,d,e,f = part['matrix']
        forward = np.array([[a,c,e],[b,d,f],[0,0,1]])
        forward[:2] *= factor
        inverse = np.linalg.inv(forward)
        image = src.transform(canvas.size, Image.Transform.AFFINE,
                              tuple(inverse[:2].ravel()), Image.Resampling.BICUBIC)
        canvas.alpha_composite(image)
    return canvas


def main():
    QA.mkdir(parents=True, exist_ok=True)
    atlas_path = ROOT / 'spritesheet.png'
    atlas = Image.open(atlas_path).convert('RGBA')
    poses, quality = [], []
    for row, count in enumerate(COUNTS):
        poses.append([])
        for column in range(count):
            frame = atlas.crop((column*192, row*208, (column+1)*192, (row+1)*208))
            targets = cell_parts(frame)
            parts = []
            for name, target in zip(NAMES, targets, strict=True):
                layer = LAYERS[name]
                part = {'image': name}
                source_rotation = None
                if name.startswith('eye'):
                    box = bbox(target > .5)
                    width, height = box[2:]-box[:2]
                    # The half-lidded failure pose clips the original eye at its top.
                    top = int(box[1])
                    top_width = np.count_nonzero(target[top] > .5)
                    widest = max(np.count_nonzero(line > .5) for line in target)
                    if width > height*1.2:
                        # A closed eye is a horizontal capsule, not a flattened
                        # vertical eye with rectangular ends.
                        source_rotation = np.array([[0,1,0],[-1,0,layer.width-1],[0,0,1]], float)
                        layer = layer.transpose(Image.Transpose.ROTATE_90)
                    elif height > width and height < width*1.9 and top_width > widest*.7:
                        cut = round(layer.height*.35)
                        part['crop'] = [0, cut, layer.width, layer.height-cut]
                        layer = layer.crop((0, cut, layer.width, layer.height))
                part['matrix'], error = fit(layer, target, name)
                if source_rotation is not None:
                    a,b,c,d,e,f = part['matrix']
                    composed = np.array([[a,c,e],[b,d,f],[0,0,1]]) @ source_rotation
                    part['matrix'] = [round(float(x),7) for x in [composed[0,0],composed[1,0],composed[0,1],composed[1,1],composed[0,2],composed[1,2]]]
                parts.append(part)
                quality.append({'row':row, 'frame':column, 'part':name, 'contour_rms_px':round(error,3)})
            poses[row].append(parts)
            rendered = paint(parts)
            rendered.save(QA / f'frame-{row:02d}-{column:02d}.png')
        print(json.dumps({'row':row, 'frames':count}), flush=True)
    (HERE/'poses.json').write_text(json.dumps(poses, separators=(',', ':'))+'\n')
    report = {'atlas_sha256':hashlib.sha256(atlas_path.read_bytes()).hexdigest(),
              'frame_counts':COUNTS, 'frames':sum(COUNTS),
              'motion_source':'Approved native atlas; all frame timing, poses and placement retained',
              'pixel_source':'Original high-resolution film rig layers',
              'assets':{name:{'dimensions':list(layer.size),'sha256':hashlib.sha256((ASSETS/f'rig-{name}.png').read_bytes()).hexdigest()} for name,layer in LAYERS.items()},
              'fits':quality}
    (QA/'pose-fitting.json').write_text(json.dumps(report, indent=2)+'\n')
    # An equal-size, 2x-display comparison, without post-render sharpening.
    comparison = Image.new('RGB', (1152, 710), '#1a1e27')
    draw = ImageDraw.Draw(comparison)
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 26)
    for i,label in enumerate(['Previous sprite, enlarged', 'High-resolution original layers']):
        draw.text((24+i*576,20), label, fill='#e9edf5', font=font)
    old = atlas.crop((0,0,192,208)).resize((576,624), Image.Resampling.BICUBIC)
    new = paint(poses[0][0])
    comparison.paste(old,(0,65),old)
    comparison.paste(new,(576,65),new)
    comparison.save(QA/'resolution-comparison.png')
    sheet = Image.new('RGB',(8*288,11*334),'#1a1e27')
    for r, row in enumerate(poses):
        for c, parts in enumerate(row):
            frame=paint(parts).resize((288,312),Image.Resampling.LANCZOS)
            sheet.paste(frame,(c*288,r*334),frame)
            ImageDraw.Draw(sheet).text((c*288+8,r*334+310),f'{r}/{c}',fill='white')
    sheet.save(QA/'hd-contact-sheet.png')
    print(json.dumps({'ok':True,'frames':sum(COUNTS),'worst_contour_rms_px':max(x['contour_rms_px'] for x in quality)}))


if __name__ == '__main__':
    main()
