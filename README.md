# Prismo

A little dark side. A lot of color.

Prismo is a small animated prism companion with floating white and rainbow hands.
It blinks, waves, glides, thinks, and takes the occasional little leap.

![Prismo cycling through its nine animations](assets/prismo.gif)

## Get Prismo

Download the [web-compatible sprite sheet](https://raw.githubusercontent.com/Audiofool934/prismo/main/spritesheet-v1.png).
In ChatGPT, where Pets are available, go to **Settings > Personalization > Pet**, choose **Upload pet**, and select the downloaded PNG.
Then choose Prismo as your pet.
See the [official Pets guide](https://learn.chatgpt.com/docs/pets) for current availability and settings.

For a Pets workflow that supports the newer v2 format, use [spritesheet.png](https://raw.githubusercontent.com/Audiofool934/prismo/main/spritesheet.png).
It includes all nine animations plus sixteen look directions.
The web-compatible v1 file contains the same nine animations, with the two look-direction rows omitted.

## Preview

Choose **Code > Download ZIP**, extract it, and open `preview.html` in a browser.
The preview works offline.
Switch between the nine animations, pause, change the backdrop, or select **Follow my pointer** to try the sixteen look directions.

## Files

| File | Contents |
| --- | --- |
| [spritesheet.png](spritesheet.png) | Full v2 sprite sheet, 1536 x 2288 pixels, 73 active frames |
| [spritesheet-v1.png](spritesheet-v1.png) | Web-compatible v1 sprite sheet, 1536 x 1872 pixels, 57 active frames |
| [preview.html](preview.html) | Self-contained interactive animation preview |
| [prismo.json](prismo.json) | Sprite dimensions, frame counts, and direction order |
| [assets/look-directions.png](assets/look-directions.png) | All sixteen look poses at native size |
| [source/](source/) | Canonical artwork and selected generated animation strips |
| [SHA256SUMS](SHA256SUMS) | Checksums for the artwork and preview |

## The design

Two white capsule eyes live inside a rounded black triangle with a pale cyan rim.
The white oval hand floats on the viewer's left, and the rainbow oval hand floats on the right.
Their outer ends tilt slightly downward, leaving a clear gap between each hand and the body.

The v2 sheet uses 192 x 208 pixel cells in eight columns.
Its first nine rows are idle, glide right, glide left, wave, jump, failed, waiting, working, and review.
The final two rows run clockwise from looking up, in 22.5-degree steps.

The artwork was made with OpenAI image generation and assembled from the selected source strips.
The final v2 sheet passed structural, transparency, eye-clearance, and floating-hand separation checks across all 73 frames.
The compatibility export preserves the first nine rows pixel for pixel.
