# Prismo for Hermes

Prismo works as a local pet in Hermes Agent and Hermes Desktop.
The package contains `prismo/pet.json` and a transparent PNG sprite sheet.
It does not require a plugin or a Petdex account.

## Install

Run these commands on the machine that runs Hermes Agent.
If Hermes Desktop connects over SSH, run them on the SSH host.
Installing on the Desktop machine alone does not install the pet on the remote Agent.

The commands below use the default profile, or the directory in `HERMES_HOME` if you have set it.
For a named profile, set `HERMES_HOME` to that profile's directory first.
You can check the target with `hermes pets doctor`.

```sh
prismo_home="${HERMES_HOME:-$HOME/.hermes}"
curl -fL https://raw.githubusercontent.com/Audiofool934/prismo/main/hermes/prismo-hermes.zip -o prismo-hermes.zip
mkdir -p "$prismo_home/pets"
unzip -n prismo-hermes.zip -d "$prismo_home/pets"
HERMES_HOME="$prismo_home" hermes pets select prismo
```

The `-n` option preserves existing files.
For an update, move the existing `pets/prismo` directory to a backup before extracting the new package.
Prismo is distributed here as a local package, so `hermes pets install prismo` is not the installation command.
That command searches the Petdex catalog.

## Hermes Desktop

Open **Settings > Appearance > Pet** on the same connection and profile.
Search for **Prismo** and select it if it is not already active.
If the list was open during installation, close Settings and reopen it to refresh the gallery.
Use the pet scale control to adjust its size.
The pet reacts to Agent activity; roaming can also play the left and right glide animations.

## Check playback

```sh
HERMES_HOME="$prismo_home" hermes pets list --installed
HERMES_HOME="$prismo_home" hermes pets doctor
HERMES_HOME="$prismo_home" hermes pets show prismo --state jump --once
```

Run `show` in an interactive terminal.
The renderer uses terminal graphics where supported and a colored text fallback otherwise.
Other state names are `idle`, `wave`, `run`, `failed`, `review`, and `waiting`.
Use `HERMES_HOME="$prismo_home" hermes pets off` to hide the pet without removing its files.

Verified with Hermes Agent 0.22.4 and Hermes Desktop 0.22.4 on macOS.
All nine rows completed an actual terminal playback run on the Agent host.
The Desktop app loaded the installed pet from that remote Agent.

## Animation format

The sheet has eight columns and nine rows of 192 x 208 pixel cells, for a total of 1536 x 1872 pixels.
Its row order is idle, glide right, glide left, wave, jump, failed, waiting, working, and review.
There are 51 active frames; unused cells stay transparent.

Hermes 0.22.4 reads at most six frames for each driven state and stops at transparent padding.
The compatibility export samples the complete eight-frame glide and failed loops into six frames.
The four-frame wave and five-frame jump stay intact, including the jump's takeoff, peak, and landing.
All retained frames preserve the approved source pixels exactly.
Hermes controls the playback speed, with a 1100 ms loop for each state.
The sixteen pointer look directions remain available in the web demo and full ChatGPT sheet; Hermes does not use those rows.

`build.py` rebuilds the PNG, metadata, and ZIP from the repository's original sprite sheet.
It requires Python 3 and Pillow.
`animation.json` records the exact source frame mapping.
The ChatGPT downloads are separate and unchanged.

See the [official Hermes pets guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/pets) for current app controls.
