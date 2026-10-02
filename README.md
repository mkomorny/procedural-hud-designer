# Procedural HUD & Schematic Designer

A procedural vector generation engine that mathematically calculates and renders production-grade aviation HUDs, targeting reticles, orbital telemetry frames, and 19-inch audio rack unit hardware faceplates in scalable SVG format.

## Procedural Generators

- **Avionics Flight Reticle**: Nested concentric range rings, cardinal degree tick-marks, dynamic horizon pitch ladders, and velocity vector arrows.
- **Targeting & Telemetry Box**: Bounding box telemetry brackets with corner reticles, micro-grid coordinates, and status callouts.
- **Audio Hardware Faceplate**: Standardized 19-inch 1U/2U rack unit panels with rotary potentiometer dials, decibel VU meter gradations, LED indicators, and mounting holes.

## Color Themes

Includes calibrated phosphor color palettes:
- `avionics`: Green phosphor (`#00ff66`) with tactical dark cockpit grids (`#030806`)
- `amber`: Flight navigation amber (`#ffb000`) with high-contrast backing (`#0d0f10`)
- `cyan`: Sci-fi naval HUD cyan (`#00e5ff`) with deep oceanic framing (`#07090c`)
- `crimson`: Threat/alert crimson (`#ff0055`) with muted ruby grids (`#0a0507`)
- `audio-rack`: Brushed dark aluminum (`#141517`) with vintage hardware indicators (`#ff5500`)

## Dependencies

- **Python**: Version 3.8+ (Standard Library: `math`, `os`, `sys`, `json`, `argparse`, `pathlib`). Zero pip dependencies.

## Instructions

See [INSTRUCTIONS.md](./INSTRUCTIONS.md) for CLI commands and preview rendering.
