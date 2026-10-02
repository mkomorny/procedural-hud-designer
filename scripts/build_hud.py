#!/usr/bin/env python3
"""
HUD & Schematic Designer Engine
Generates mathematical vector graphics for sci-fi HUDs, avionics displays, radar reticles, and audio rack faceplates.
"""

import sys
import os
import math
import json
import argparse
from pathlib import Path

COLOR_THEMES = {
    "avionics": {"fg": "#00ff66", "bg": "#030806", "accent": "#00ffcc", "grid": "#082a15"},
    "amber": {"fg": "#ffb000", "bg": "#0d0f10", "accent": "#ffe066", "grid": "#2b1c00"},
    "cyan": {"fg": "#00e5ff", "bg": "#07090c", "accent": "#3fd0e0", "grid": "#0d222e"},
    "crimson": {"fg": "#ff0055", "bg": "#0a0507", "accent": "#ff5588", "grid": "#2b0a14"},
    "audio-rack": {"fg": "#d0d0ce", "bg": "#141517", "accent": "#ff5500", "grid": "#24262b"}
}

def generate_radar_reticle(theme="avionics", size=400):
    t = COLOR_THEMES.get(theme, COLOR_THEMES["avionics"])
    cx, cy = size / 2, size / 2
    r_max = (size / 2) - 20
    
    elements = []
    # Background circle
    elements.append(f'<circle cx="{cx}" cy="{cy}" r="{r_max}" fill="{t["bg"]}" stroke="{t["fg"]}" stroke-width="1.5" />')
    
    # Concentric rings
    for factor in [0.25, 0.5, 0.75]:
        r = r_max * factor
        elements.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["fg"]}" stroke-width="0.75" stroke-dasharray="3,3" opacity="0.6" />')
        
    # Crosshairs
    elements.append(f'<line x1="{cx - r_max}" y1="{cy}" x2="{cx + r_max}" y2="{cy}" stroke="{t["fg"]}" stroke-width="1" opacity="0.8" />')
    elements.append(f'<line x1="{cx}" y1="{cy - r_max}" x2="{cx}" y2="{cy + r_max}" stroke="{t["fg"]}" stroke-width="1" opacity="0.8" />')
    
    # 360-degree tick marks
    for deg in range(0, 360, 10):
        rad = math.radians(deg)
        tick_len = 10 if deg % 30 == 0 else 5
        x1 = cx + (r_max - tick_len) * math.cos(rad)
        y1 = cy + (r_max - tick_len) * math.sin(rad)
        x2 = cx + r_max * math.cos(rad)
        y2 = cy + r_max * math.sin(rad)
        sw = 1.25 if deg % 30 == 0 else 0.75
        elements.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{t["fg"]}" stroke-width="{sw}" />')
        
    # Degree labels on 0, 90, 180, 270
    labels = [(0, "090°", cx + r_max - 28, cy - 4), (90, "180°", cx - 14, cy + r_max - 14), (180, "270°", cx - r_max + 6, cy - 4), (270, "000°", cx - 14, cy - r_max + 22)]
    for _, text, lx, ly in labels:
        elements.append(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="{t["accent"]}" font-family="monospace" font-size="10" font-weight="bold">{text}</text>')
        
    # Sweeping radar arm with gradient blip
    angle = 45
    rad = math.radians(angle)
    x_sweep = cx + r_max * math.cos(rad)
    y_sweep = cy + r_max * math.sin(rad)
    elements.append(f'<line x1="{cx}" y1="{cy}" x2="{x_sweep:.1f}" y2="{y_sweep:.1f}" stroke="{t["accent"]}" stroke-width="2" />')
    # Simulated blips
    blip_x, blip_y = cx + (r_max * 0.55) * math.cos(math.radians(35)), cy + (r_max * 0.55) * math.sin(math.radians(35))
    elements.append(f'<circle cx="{blip_x:.1f}" cy="{blip_y:.1f}" r="3.5" fill="{t["accent"]}" />')
    elements.append(f'<circle cx="{blip_x:.1f}" cy="{blip_y:.1f}" r="7" fill="none" stroke="{t["accent"]}" stroke-width="1" opacity="0.6" />')
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
  <style>
    text {{ user-select: none; }}
  </style>
  {"\n  ".join(elements)}
</svg>"""
    return svg

def generate_telemetry_frame(theme="cyan", width=600, height=350):
    t = COLOR_THEMES.get(theme, COLOR_THEMES["cyan"])
    elements = []
    
    # Background rect
    elements.append(f'<rect width="{width}" height="{height}" fill="{t["bg"]}" />')
    
    # Corner brackets (Beveled frame)
    cut = 24
    points = f"{cut},10 {width-cut},10 {width-10},{cut} {width-10},{height-cut} {width-cut},{height-10} {cut},{height-10} 10,{height-cut} 10,{cut}"
    elements.append(f'<polygon points="{points}" fill="none" stroke="{t["fg"]}" stroke-width="1.5" />')
    
    # Technical outer grid border
    elements.append(f'<rect x="18" y="18" width="{width-36}" height="{height-36}" fill="none" stroke="{t["grid"]}" stroke-width="0.75" />')
    
    # Corner L-brackets
    b_len = 16
    corners = [
        (4, 4, 4+b_len, 4, 4, 4+b_len),
        (width-4, 4, width-4-b_len, 4, width-4, 4+b_len),
        (width-4, height-4, width-4-b_len, height-4, width-4, height-4-b_len),
        (4, height-4, 4+b_len, height-4, 4, height-4-b_len)
    ]
    for x1, y1, x2, y2, x3, y3 in corners:
        elements.append(f'<polyline points="{x2},{y2} {x1},{y1} {x3},{y3}" fill="none" stroke="{t["accent"]}" stroke-width="2" />')
        
    # Header technical bar
    elements.append(f'<rect x="28" y="24" width="120" height="14" fill="{t["accent"]}" opacity="0.15" />')
    elements.append(f'<text x="32" y="35" fill="{t["accent"]}" font-family="monospace" font-size="9" font-weight="bold">SYSTEM TELEMETRY [ACTIVE]</text>')
    elements.append(f'<text x="{width-140}" y="35" fill="{t["fg"]}" font-family="monospace" font-size="9" opacity="0.8">CH: 04 // REF: 99.42 Hz</text>')
    
    # Caliper scales on right side
    for i in range(10):
        y = 60 + (i * 22)
        w_mark = 8 if i % 2 == 0 else 4
        elements.append(f'<line x1="{width-26}" y1="{y}" x2="{width-26+w_mark}" y2="{y}" stroke="{t["fg"]}" stroke-width="1" />')
        
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  {"\n  ".join(elements)}
</svg>"""
    return svg

def generate_rack_faceplate(theme="audio-rack", width=800, height=200):
    t = COLOR_THEMES.get(theme, COLOR_THEMES["audio-rack"])
    elements = []
    
    # Main 19-inch 2U rack chassis
    elements.append(f'<rect width="{width}" height="{height}" rx="3" fill="{t["bg"]}" stroke="{t["fg"]}" stroke-width="2" />')
    
    # Rack mount ear screw holes (Left and Right)
    for x_hole in [22, width - 22]:
        for y_hole in [35, height - 35]:
            elements.append(f'<circle cx="{x_hole}" cy="{y_hole}" r="8" fill="#000" stroke="{t["fg"]}" stroke-width="1.5" />')
            elements.append(f'<line x1="{x_hole-5}" y1="{y_hole}" x2="{x_hole+5}" y2="{y_hole}" stroke="{t["fg"]}" stroke-width="1" />')
            
    # Silkscreen dividing line separating ears from chassis panel
    elements.append(f'<line x1="48" y1="10" x2="48" y2="{height-10}" stroke="{t["grid"]}" stroke-width="1.5" />')
    elements.append(f'<line x1="{width-48}" y1="10" x2="{width-48}" y2="{height-10}" stroke="{t["grid"]}" stroke-width="1.5" />')
    
    # Device Title
    elements.append(f'<text x="64" y="38" fill="{t["fg"]}" font-family="monospace" font-size="13" font-weight="bold" letter-spacing="2">SPECTRAL HARMONIC COMPRESSOR</text>')
    elements.append(f'<text x="64" y="52" fill="{t["accent"]}" font-family="monospace" font-size="9" letter-spacing="1">MODEL SC-102 // CLASS-A DISCRETE</text>')
    
    # 4 Rotary Knobs with tick collars
    knob_labels = ["INPUT GAIN", "THRESHOLD", "RATIO", "OUTPUT"]
    knob_start_x = 360
    for i, label in enumerate(knob_labels):
        kx = knob_start_x + (i * 95)
        ky = 105
        # Tick marks collar around knob
        for deg in range(135, 415, 25):
            rad = math.radians(deg)
            x1 = kx + 26 * math.cos(rad)
            y1 = ky + 26 * math.sin(rad)
            x2 = kx + 30 * math.cos(rad)
            y2 = ky + 30 * math.sin(rad)
            elements.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{t["fg"]}" stroke-width="1" />')
        # Knob Body
        elements.append(f'<circle cx="{kx}" cy="{ky}" r="22" fill="#1e2024" stroke="{t["fg"]}" stroke-width="1.5" />')
        # Pointer notch
        deg_val = 135 + (i * 45)
        rad_val = math.radians(deg_val)
        px = kx + 20 * math.cos(rad_val)
        py = ky + 20 * math.sin(rad_val)
        elements.append(f'<line x1="{kx}" y1="{ky}" x2="{px:.1f}" y2="{py:.1f}" stroke="{t["accent"]}" stroke-width="2.5" />')
        # Label
        elements.append(f'<text x="{kx}" y="{ky + 45}" fill="{t["fg"]}" font-family="monospace" font-size="8" text-anchor="middle" font-weight="bold">{label}</text>')
        
    # VU Meter Section (Left center)
    elements.append(f'<rect x="64" y="70" width="180" height="85" rx="4" fill="#08090a" stroke="{t["grid"]}" stroke-width="1.5" />')
    elements.append(f'<text x="74" y="86" fill="{t["accent"]}" font-family="monospace" font-size="9" font-weight="bold">GAIN REDUCTION (dB)</text>')
    # VU bar segments
    for bar in range(16):
        bx = 74 + (bar * 10)
        by = 100
        color = t["accent"] if bar < 10 else "#e63946"
        elements.append(f'<rect x="{bx}" y="{by}" width="7" height="35" fill="{color}" opacity="{0.9 if bar < 11 else 0.2}" />')
        
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  {"\n  ".join(elements)}
</svg>"""
    return svg

def build_hud(component_type, theme, out_path):
    if component_type == "radar":
        svg_content = generate_radar_reticle(theme=theme)
    elif component_type == "frame":
        svg_content = generate_telemetry_frame(theme=theme)
    elif component_type == "rack":
        svg_content = generate_rack_faceplate(theme=theme)
    else:
        svg_content = generate_radar_reticle(theme=theme)
        
    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    # Generate HTML preview
    preview_file = out_file.parent / f"{out_file.stem}_preview.html"
    t = COLOR_THEMES.get(theme, COLOR_THEMES["avionics"])
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>HUD Preview · {component_type}</title>
  <style>
    body {{
      background: {t['bg']};
      color: {t['fg']};
      margin: 0;
      padding: 3rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      font-family: monospace;
    }}
    .hud-box {{
      box-shadow: 0 0 30px {t['accent']}33;
      border: 1px solid {t['fg']}44;
      padding: 1.5rem;
      background: rgba(0,0,0,0.5);
      border-radius: 8px;
      max-width: 95vw;
    }}
    h2 {{ margin-bottom: 1rem; color: {t['accent']}; font-size: 1.1rem; }}
  </style>
</head>
<body>
  <div class="hud-box">
    <h2>SCHEMATIC: {component_type.upper()} [{theme.upper()}]</h2>
    {svg_content}
  </div>
</body>
</html>"""
    with open(preview_file, "w", encoding="utf-8") as f:
        f.write(html)
        
    return out_file, preview_file

def main():
    parser = argparse.ArgumentParser(description="Generate procedural HUD and schematic vector graphics.")
    parser.add_argument("--type", choices=["radar", "frame", "rack"], default="radar", help="HUD component type")
    parser.add_argument("--theme", choices=["avionics", "amber", "cyan", "crimson", "audio-rack"], default="avionics", help="Color theme")
    parser.add_argument("--out", default="./hud_output.svg", help="Output file path")
    args = parser.parse_args()
    
    svg_f, html_f = build_hud(args.type, args.theme, args.out)
    res = {
        "status": "success",
        "svg_path": str(svg_f.resolve()),
        "preview_path": str(html_f.resolve()),
        "type": args.type,
        "theme": args.theme
    }
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
