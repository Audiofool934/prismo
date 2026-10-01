# Source artwork

[canonical.png](canonical.png) defines Prismo's shape, eye construction, palette, and detached oval hands.
The files in [strips/](strips/) are the selected generated sources for the final design.
Their magenta backgrounds are an extraction aid; the finished sprite sheets are transparent.

## Animation strips

| File | Poses |
| --- | ---: |
| `idle.png` | 6 |
| `running-right.png` | 8 |
| `running-left.png` | 8 |
| `waving.png` | 4 |
| `jumping.png` | 5 |
| `failed.png` | 8 |
| `waiting.png` | 6 |
| `running.png` | 6 |
| `review.png` | 6 |

The filenames follow the Pets animation-state names.
Prismo glides for directional movement and uses eye and hand gestures for the working state.
It has no feet or connecting arms.

## Look directions

`look-cardinals.png` is the four-pose reference strip, in the order up, right, down, left.
`look-row-9.png` contains 000, 022.5, 045, 067.5, 090, 112.5, 135, and 157.5 degrees.
`look-row-10.png` contains 180, 202.5, 225, 247.5, 270, 292.5, 315, and 337.5 degrees.
Angles are clockwise from up in viewer coordinates.

The eyes translate together as a level pair inside the black face.
The triangle and hands keep their positions during gaze changes.
Some intermediate eye steps are deliberately subtle; the four main directions were independently checked for readability.

## Assembly

The finished atlas uses generated pixels from these sources.
The strips were extracted, scaled with consistent proportions, registered, and cleaned of their magenta backgrounds.
The final placement aligns the tops of the resting eyes with the horizontal centerline at y = 104 in each 192 x 208 pixel cell.
The jump rises 46 pixels before returning to its original baseline, leaving the full character inside the cell.
The low hand placement, separate oval shapes, and visible gaps are part of the character design.

For installation, use the finished sprite sheet in the repository root.
These larger source strips are intended for inspecting or continuing the artwork.
