#!/usr/bin/env python3
"""
Example script demonstrating how to create test images and generate a sprite set.
This creates sample marker icons and packages them into a sprite set.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw

def create_sample_icon(name: str, color: tuple, size: int = 32) -> Image.Image:
    """Create a simple sample icon."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw circle
    padding = 4
    draw.ellipse(
        [padding, padding, size - padding, size - padding],
        fill=color,
        outline=(255, 255, 255, 200),
        width=2
    )
    
    # Add a simple symbol in the center
    center = size // 2
    symbol_size = size // 4
    
    if 'marker' in name:
        # Draw a pin shape
        draw.ellipse(
            [center - symbol_size//2, center - symbol_size//2, 
             center + symbol_size//2, center + symbol_size//2],
            fill=(255, 255, 255, 255)
        )
    elif 'building' in name:
        # Draw a square
        draw.rectangle(
            [center - symbol_size//2, center - symbol_size//2,
             center + symbol_size//2, center + symbol_size//2],
            fill=(255, 255, 255, 255)
        )
    elif 'park' in name:
        # Draw a triangle
        draw.polygon(
            [(center, center - symbol_size//2),
             (center - symbol_size//2, center + symbol_size//2),
             (center + symbol_size//2, center + symbol_size//2)],
            fill=(255, 255, 255, 255)
        )
    
    return img

def create_sample_images():
    """Create a set of sample images for testing."""
    sample_dir = Path('./sample_icons')
    sample_dir.mkdir(exist_ok=True)
    
    print("Creating sample images...")
    
    # Define sample icons
    icons = [
        ('location-marker', (255, 87, 51)),      # Red-orange
        ('building', (52, 152, 219)),             # Blue
        ('park', (46, 204, 113)),                 # Green
        ('school', (241, 196, 15)),               # Yellow
        ('hospital', (231, 76, 60)),              # Red
        ('restaurant', (155, 89, 182)),           # Purple
        ('shop', (26, 188, 156)),                 # Turquoise
        ('transport', (52, 73, 94)),              # Dark blue
    ]
    
    for name, color in icons:
        img = create_sample_icon(name, color)
        img.save(sample_dir / f"{name}.png")
        print(f"  Created: {name}.png")
    
    print(f"\nSample images created in: {sample_dir}")
    return sample_dir

def main():
    """Run the example."""
    print("=== OpenHistorical Map Sprite Set Example ===\n")
    
    # Create sample images
    sample_dir = create_sample_images()
    
    print("\nNow run the sprite set generator:")
    print(f"  python create_sprite_set.py {sample_dir}\n")
    print("Or try with custom options:")
    print(f"  python create_sprite_set.py {sample_dir} map-icons --pixel-ratio 2\n")

if __name__ == '__main__':
    main()
