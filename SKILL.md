---
name: hud-schematic-designer
description: Procedurally generates production-grade vector HUDs, avionics radar reticles, telemetry frames, and 19-inch audio rack unit faceplates (SVGs with interactive HTML previews) styled to match your design themes. Triggered in chat whenever the user asks for HUD graphics, radar circles, telemetry borders, or audio hardware faceplates.
---

# HUD & Schematic Designer

Generates precision mathematical vector graphics (SVGs) for futuristic user interfaces, telemetry viewports, radar reticles, and hardware audio synthesizer rack faceplates.

Whenever the user asks for sci-fi HUDs, avionics graphics, tech borders, or audio rack chassis designs, activate this skill.

---

## When to Activate

Trigger this skill whenever the user says things like:
* *"Design a glowing radar reticle for my avionics dashboard."*
* *"Make a futuristic HUD frame with corner brackets and telemetry coordinates in cyan."*
* *"Generate an audio rack faceplate with knobs and VU meters for a synth project."*
* *"Create a sci-fi schematic blueprint border."*
* *"Build a technical oscilloscope or targeting circle in SVG."*

---

## Component Types Supported

1. **`radar` (Radar Reticle & Targeting Compass):** Concentric range rings, 360-degree tick marks, crosshairs, azimuth degree readouts (`090°`, `180°`, `270°`, `000°`), and sweeping radar scan arm with signal blips.
2. **`frame` (Telemetry Viewport & Caliper Border):** Beveled corner polygon frames, technical L-brackets, caliper scale ticks, and status indicator readouts.
3. **`rack` (19-Inch Audio Rack Faceplate):** Standard 19" 2U rackmount chassis with mounting screw ears, 4 rotary potentiometer knobs with angle ticks, gain reduction VU meter bars, and silkscreen labels.

---

## Color Themes Supported

* **`avionics`:** CRT Phosphor Green (`#00ff66`) on pitch black (`#030806`).
* **`amber`:** 1980s Terminal Amber (`#ffb000`) on dark CRT glass (`#0d0f10`).
* **`cyan`:** High-tech Cyberdeck Cyan (`#00e5ff`) on deep space (`#07090c`).
* **`crimson`:** High-threat / Red Alert (`#ff0055`) on dark slate (`#0a0507`).
* **`audio-rack`:** Industrial brushed dark aluminum (`#141517`) with signal orange indicators (`#ff5500`).

---

## How to Execute Under the Hood (Silent Agent Workflow)

You do **NOT** ask the user to run scripts in PowerShell. Run the generator invisibly using terminal/bash commands:

```bash
# Generate radar reticle:
python "<skill_dir>/scripts/build_hud.py" --type "radar" --theme "avionics" --out "./hud_radar.svg"

# Generate telemetry frame:
python "<skill_dir>/scripts/build_hud.py" --type "frame" --theme "cyan" --out "./hud_frame.svg"

# Generate audio rack faceplate:
python "<skill_dir>/scripts/build_hud.py" --type "rack" --theme "audio-rack" --out "./audio_rack_faceplate.svg"
```

The script automatically generates:
1. The standalone `.svg` vector asset.
2. An interactive `_preview.html` showcase file featuring glowing ambient light effects and responsive centering.

---

## Chat Presentation Guidelines

When presenting the generated HUD in chat:
1. **Provide the Clickable Links:**
   * Direct link to the SVG file: `[schematic.svg](file:///...)`
   * Direct link to the HTML visual preview: `[preview.html](file:///...)`
2. **Component Specs:** Detail the dimensions, color theme, and component elements (knobs, reticles, tick intervals).
3. **Usage Tip:** Tell the user how they can drop the SVG straight into their web app, Electron UI, or Max for Live device skin.
