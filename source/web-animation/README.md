# High-resolution web animation

The web demo draws five original high-resolution image layers onto a canvas sized for the visitor's display.
The body is 855 x 757 pixels; the hands and eyes retain their original source resolution.
These are the same image layers used in the Prismo film, with the approved outline, colors, and floating hands.

`poses.json` holds the layer transforms for all 73 poses, measured from the native pet sheet.
The nine animation states, frame counts, timing, centered placement, and sixteen gaze directions are retained.
The web artwork is composed from these layers instead of enlarging the 192 x 208 pixel pet frames.
The downloadable pet sheets retain their required dimensions and original pixels.

`renderer.js` draws only when the pose or display size changes.
Its backing canvas follows the displayed size and device pixel ratio, up to 4x.
It does not allocate an enlarged multi-frame texture or add a framework dependency.

To rebuild `docs/index.html` and the self-contained `preview.html`, run:

```sh
python3 source/web-animation/render_preview.py
```

The editable page lives in `template.html`.
Artwork, pose data, renderer, and the Floydian font are embedded during packaging so the preview also works offline.

`build_poses.py` optionally regenerates the pose transforms from `spritesheet.png` and the layers.
It requires Pillow, NumPy, and SciPy, and writes comparison images and measurements into the ignored `qa/` directory.
Review those outputs before replacing an approved set of poses.
