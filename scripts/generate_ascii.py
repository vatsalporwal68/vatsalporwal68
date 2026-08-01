#!/usr/bin/env python3
"""
Generate Self-Typing Animated ASCII Portrait SVG
Converts a photo into a dark/light mode compatible animated SMIL SVG.
Supports OpenCV/rembg pipeline with standard PIL fallback.
"""

import sys
import os
import argparse
import math

RAMP = list(" .`:-=+*cs#%@")

def process_image_pil(img_path, cols=90):
    try:
        from PIL import Image, ImageEnhance, ImageFilter
    except ImportError:
        print("[!] Pillow is required. Installing or running fallback...")
        sys.exit(1)

    img = Image.open(img_path).convert("L")
    w, h = img.size
    rows = int(cols * (h / w) * 0.48)
    img = img.resize((cols, rows), Image.Resampling.LANCZOS)
    
    # Contrast enhancement & edge preservation
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.8)
    
    pixels = img.load()
    lines = []
    num_chars = len(RAMP)
    
    for r in range(rows):
        line_chars = []
        for c in range(cols):
            val = pixels[c, r]
            # Darkening curve (v/255)^1.7
            norm = (val / 255.0) ** 1.7
            idx = int(norm * num_chars)
            idx = min(max(idx, 0), num_chars - 1)
            line_chars.append(RAMP[idx])
        lines.append("".join(line_chars))
        
    return lines, cols, rows

def process_image(img_path, cols=90):
    try:
        import cv2
        import numpy as np

        img_bgr = cv2.imread(img_path)
        if img_bgr is None:
            return process_image_pil(img_path, cols)

        h, w = img_bgr.shape[:2]

        try:
            from rembg import remove
            from PIL import Image
            pil_img = Image.open(img_path).convert("RGBA")
            no_bg = remove(pil_img)
            white_bg = Image.new("RGBA", no_bg.size, (255, 255, 255, 255))
            composite = Image.alpha_composite(white_bg, no_bg).convert("RGB")
            img_bgr = cv2.cvtColor(np.array(composite), cv2.COLOR_RGB2BGR)
            print("[+] Background successfully removed using rembg.")
        except Exception as e:
            print(f"[!] rembg background removal skipped ({e}).")

        rows = int(cols * (h / w) * 0.48)
        img_resized = cv2.resize(img_bgr, (cols, rows), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

        filtered = cv2.bilateralFilter(gray, d=5, sigmaColor=75, sigmaSpace=75)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        equalized = clahe.apply(filtered)

        darkened = np.power(equalized / 255.0, 1.7) * 255.0
        darkened = np.clip(darkened, 0, 255).astype(np.uint8)

        num_chars = len(RAMP)
        lines = []
        for r in range(rows):
            line_chars = []
            for c in range(cols):
                val = darkened[r, c]
                idx = int(val / 256.0 * num_chars)
                idx = min(idx, num_chars - 1)
                line_chars.append(RAMP[idx])
            lines.append("".join(line_chars))

        return lines, cols, rows

    except Exception:
        print("[!] OpenCV/numpy not available. Falling back to PIL processing.")
        return process_image_pil(img_path, cols)

def generate_svg(lines, cols, rows, output_path):
    char_w = 7.74
    char_h = 13.5
    padding = 20
    
    total_w = int(cols * char_w + padding * 2)
    total_h = int(rows * char_h + padding * 2)

    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {total_h}" width="{total_w}" height="{total_h}">')
    svg_lines.append('  <style>')
    svg_lines.append('    .ascii-text { font-family: "Courier New", Consolas, "Liberation Mono", monospace; font-size: 12.9px; fill: #24292e; white-space: pre; }')
    svg_lines.append('    @media (prefers-color-scheme: dark) { .ascii-text { fill: #c9d1d9; } }')
    svg_lines.append('  </style>')
    
    svg_lines.append('  <defs>')
    for i in range(rows):
        y = padding + i * char_h
        delay = round(i * 0.09, 2)
        dur = 0.35
        svg_lines.append(f'    <clipPath id="cp-{i}">')
        svg_lines.append(f'      <rect x="{padding}" y="{y:.1f}" width="0" height="{char_h:.1f}">')
        svg_lines.append(f'        <animate attributeName="width" from="0" to="{cols * char_w:.1f}" dur="{dur}s" begin="{delay}s" fill="freeze" />')
        svg_lines.append(f'      </rect>')
        svg_lines.append(f'    </clipPath>')
    svg_lines.append('  </defs>')

    for i, line in enumerate(lines):
        y = padding + (i + 1) * char_h - 2.5
        escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        svg_lines.append(f'  <g clip-path="url(#cp-{i})">')
        svg_lines.append(f'    <text x="{padding}" y="{y:.1f}" class="ascii-text">{escaped_line}</text>')
        svg_lines.append(f'  </g>')

    svg_lines.append('</svg>')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(svg_lines))

    print(f"[+] ASCII SVG portrait generated at '{output_path}' ({cols}x{rows} lines).")

def generate_sample_ppm(filename="portrait.jpg"):
    # Generate simple PPM/PBM fallback image without extra libraries
    cols, rows = 300, 300
    header = f"P2\n{cols} {rows}\n255\n"
    pixels = []
    cx, cy = 150, 150
    for r in range(rows):
        row = []
        for c in range(cols):
            dist = math.sqrt((c - cx)**2 + (r - cy)**2)
            if dist < 80:
                val = 40  # dark face center
            elif dist < 120:
                val = 180 # face outer
            else:
                val = 240 # white bg
            row.append(str(int(val)))
        pixels.append(" ".join(row))
    
    # Save as PGM format which PIL can read natively
    pgm_file = "portrait.pgm"
    with open(pgm_file, "w") as f:
        f.write(header + "\n".join(pixels))
    return pgm_file

def main():
    parser = argparse.ArgumentParser(description="Generate SMIL animated ASCII portrait SVG")
    parser.add_argument("--input", "-i", default="portrait.jpg", help="Path to input photo")
    parser.add_argument("--output", "-o", default="assets/portrait.svg", help="Output SVG path")
    parser.add_argument("--cols", "-c", type=int, default=90, help="Number of ASCII columns (default: 90)")
    
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[!] Input image '{args.input}' not found. Creating sample image...")
        args.input = generate_sample_ppm()

    lines, cols, rows = process_image(args.input, cols=args.cols)
    generate_svg(lines, cols, rows, args.output)

if __name__ == "__main__":
    main()
