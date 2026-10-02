# Procedural HUD Designer - Setup & Usage Guide

## Prerequisites
- **Python**: 3.8+

---

## 1. Generating Vectors via CLI

Generate a 400x400 tactical radar reticle in green avionics phosphor:
```bash
python scripts/build_hud.py --type reticle --theme avionics --size 400 --output reticle.svg
```

Generate an amber aerospace telemetry overlay:
```bash
python scripts/build_hud.py --type telemetry --theme amber --size 600 --output telemetry.svg
```

Generate a 19-inch audio hardware rack unit faceplate:
```bash
python scripts/build_hud.py --type rack --theme audio-rack --output faceplate.svg
```
