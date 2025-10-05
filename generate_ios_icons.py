#!/usr/bin/env python3
"""
Generate iOS PWA icons from SVG source.
Converts icon-512.svg to PNG files in all required iOS sizes.
"""

import os
from pathlib import Path
from cairosvg import svg2png

# iOS PWA icon sizes (comprehensive list)
IOS_SIZES = [
    40,    # Spotlight iOS 7-13
    58,    # Settings iOS 7-13 (2x)
    60,    # Home screen iOS 7-13 (2x)
    76,    # iPad Home screen iOS 7-13
    80,    # Spotlight iPad iOS 7-13 (2x)
    87,    # Settings iOS 7-13 (3x)
    114,   # Home screen iOS 6 (2x)
    120,   # Home screen iOS 7-13 (2x/3x)
    128,   # iTunes icon
    136,   # Apple Watch
    152,   # iPad Home screen iOS 7-13 (2x)
    167,   # iPad Pro (2x)
    180,   # Home screen iOS 7-13 (3x)
    192,   # Android Chrome
    1024,  # App Store
]

def generate_icons():
    """Generate all iOS icon sizes from the source SVG."""
    script_dir = Path(__file__).parent
    svg_path = script_dir / "icons" / "icon-512.svg"
    icons_dir = script_dir / "icons"

    if not svg_path.exists():
        print(f"Error: Source SVG not found at {svg_path}")
        return

    print(f"Generating iOS icons from {svg_path.name}...")

    for size in IOS_SIZES:
        output_path = icons_dir / f"apple-touch-icon-{size}x{size}.png"

        print(f"  Generating {size}x{size}...", end=" ")

        svg2png(
            url=str(svg_path),
            write_to=str(output_path),
            output_width=size,
            output_height=size
        )

        print(f"✓ {output_path.name}")

    print(f"\nSuccessfully generated {len(IOS_SIZES)} iOS icons!")

if __name__ == "__main__":
    generate_icons()
