# Prismo on Petdex

This is Prismo's distribution package for the Petdex gallery.
The package contains `pet.json` and `spritesheet.png`.
Submitted on October 22, 2026 under CC BY 4.0 and approved on October 26, 2026.
[Prismo is publicly available on Petdex](https://petdex.dev/pets/prismo) as entry #5161.
Public catalog search, installation, and all nine animation rows were verified with Hermes Agent 0.22.5.
For Hermes adoption, search for Prismo in the app's pet gallery or follow the [installation guide](../hermes/README.md#install-from-petdex).

## Format

The transparent PNG uses the standard v1 atlas: 1536 x 1872 pixels, with 192 x 208 pixel cells in eight columns and nine rows.
The rows contain 6, 8, 8, 4, 5, 8, 6, 6, and 6 populated cells.

The first six frames match the [tested Hermes export](../hermes/) pixel for pixel.
The two additional cells in each eight-frame row hold its final pose, so Petdex plays every expected cell and Hermes retains a complete loop.
No artwork is resized or redrawn.
The original ChatGPT sheets remain available at the repository root.

Run `python3 petdex/build.py` from the repository root to rebuild this package.
The build requires Pillow and uses the Hermes export as its source.

## Artwork license

Prismo artwork is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) (CC BY 4.0).
Credit **Audiofool**, link to [Prismo](https://github.com/Audiofool934/prismo) and the license, and indicate any changes.
The artwork was made with OpenAI image generation and assembled from selected source strips.
Its prism and spectrum imagery is inspired by Pink Floyd's *The Dark Side of the Moon*.
