#!/usr/bin/env python3
"""
OpenHistorical Map Sprite Set Generator

This script packages all images in a directory into a sprite sheet
along with the required JSON metadata file compatible with OpenHistorical Map format.

Usage:
    python create_sprite_set.py <input_directory> [output_name] [--pixel-ratio <ratio>] [--max-size <size>]

Arguments:
    input_directory: Directory containing images to package
    output_name: Name for the sprite set (default: 'sprites')
    --pixel-ratio: Pixel ratio for the sprite (default: 1, options: 1, 2, 4)
    --max-size: Maximum dimension for sprite sheet (default: 2048)
"""

import os
import sys
import json
import argparse
from pathlib import Path
from PIL import Image
from typing import List, Tuple, Dict


class SpritePacker:
    def __init__(self, max_width: int = 2048, max_height: int = 2048, padding: int = 2):
        self.max_width = max_width
        self.max_height = max_height
        self.padding = padding
        self.sprites: List[Dict] = []
        
    def pack_sprites(self, images: List[Tuple[str, Image.Image]]) -> Tuple[Image.Image, Dict]:
        """
        Pack images into a single sprite sheet using a simple shelf packing algorithm.
        Returns the sprite sheet image and metadata dictionary.
        """
        # Sort images by height (descending) for better packing
        sorted_images = sorted(images, key=lambda x: x[1].height, reverse=True)
        
        # Calculate total area needed
        total_area = sum(img.width * img.height for _, img in sorted_images)
        
        # Start with a reasonable size
        current_width = min(self.max_width, max(img.width for _, img in sorted_images) + 2 * self.padding)
        current_height = min(self.max_height, int((total_area / current_width) * 1.5))
        
        # Try to pack, increasing size if needed
        while current_height <= self.max_height:
            result = self._try_pack(sorted_images, current_width, current_height)
            if result:
                return result
            current_height = min(current_height + 256, self.max_height)
        
        # If still doesn't fit, try increasing width
        current_width = min(self.max_width, current_width + 512)
        current_height = 512
        
        while current_width <= self.max_width and current_height <= self.max_height:
            result = self._try_pack(sorted_images, current_width, current_height)
            if result:
                return result
            current_height = min(current_height + 256, self.max_height)
        
        raise ValueError(f"Cannot fit all images within {self.max_width}x{self.max_height} sprite sheet")
    
    def _try_pack(self, images: List[Tuple[str, Image.Image]], width: int, height: int) -> Tuple[Image.Image, Dict]:
        """Try to pack images into given dimensions."""
        sprite_sheet = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        sprite_metadata = {}
        
        # Shelf packing algorithm
        current_x = self.padding
        current_y = self.padding
        shelf_height = 0
        
        for name, img in images:
            img_width, img_height = img.size
            
            # Check if image fits on current shelf
            if current_x + img_width + self.padding > width:
                # Move to next shelf
                current_x = self.padding
                current_y += shelf_height + self.padding
                shelf_height = 0
            
            # Check if we've run out of vertical space
            if current_y + img_height + self.padding > height:
                return None  # Doesn't fit
            
            # Place the image
            sprite_sheet.paste(img, (current_x, current_y), img if img.mode == 'RGBA' else None)
            
            # Store metadata
            sprite_metadata[name] = {
                "x": current_x,
                "y": current_y,
                "width": img_width,
                "height": img_height,
                "pixelRatio": 1
            }
            
            # Update position
            current_x += img_width + self.padding
            shelf_height = max(shelf_height, img_height)
        
        # Crop to actual used size
        actual_height = current_y + shelf_height + self.padding
        if actual_height < height:
            sprite_sheet = sprite_sheet.crop((0, 0, width, actual_height))
        
        return sprite_sheet, sprite_metadata


def load_images_from_directory(directory: Path) -> List[Tuple[str, Image.Image]]:
    """Load all images from a directory."""
    supported_formats = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
    images = []
    
    for file_path in sorted(directory.iterdir()):
        if file_path.is_file() and file_path.suffix.lower() in supported_formats:
            try:
                img = Image.open(file_path)
                # Convert to RGBA for consistency
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Use filename without extension as sprite name
                sprite_name = file_path.stem
                images.append((sprite_name, img))
                print(f"Loaded: {file_path.name} ({img.width}x{img.height})")
            except Exception as e:
                print(f"Warning: Could not load {file_path.name}: {e}")
    
    return images


def create_sprite_set(input_dir: Path, output_name: str, pixel_ratio: int = 1, max_size: int = 2048):
    """Create a sprite set from images in a directory."""
    print(f"\n=== Creating OpenHistorical Map Sprite Set ===")
    print(f"Input directory: {input_dir}")
    print(f"Output name: {output_name}")
    print(f"Pixel ratio: {pixel_ratio}")
    print(f"Max size: {max_size}x{max_size}")
    print()
    
    # Load images
    images = load_images_from_directory(input_dir)
    
    if not images:
        print("Error: No valid images found in directory!")
        return False
    
    print(f"\nFound {len(images)} images")
    
    # Pack sprites
    print("\nPacking sprites...")
    packer = SpritePacker(max_width=max_size, max_height=max_size)
    
    try:
        sprite_sheet, sprite_metadata = packer.pack_sprites(images)
        print(f"Sprite sheet size: {sprite_sheet.width}x{sprite_sheet.height}")
    except ValueError as e:
        print(f"Error: {e}")
        return False
    
    # Determine output file suffix based on pixel ratio
    suffix = f"@{pixel_ratio}x" if pixel_ratio > 1 else ""
    
    # Save sprite sheet
    sprite_image_path = input_dir / f"{output_name}{suffix}.png"
    sprite_sheet.save(sprite_image_path, 'PNG', optimize=True)
    print(f"\nSaved sprite sheet: {sprite_image_path}")
    
    # Create JSON metadata
    json_data = {}
    for name, metadata in sprite_metadata.items():
        json_data[name] = metadata
        if pixel_ratio > 1:
            json_data[name]["pixelRatio"] = pixel_ratio
    
    # Save JSON
    json_path = input_dir / f"{output_name}.json"
    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"Saved sprite metadata: {json_path}")
    
    print(f"\n=== Sprite Set Created Successfully ===")
    print(f"Sprites: {len(images)}")
    print(f"Sheet size: {sprite_sheet.width}x{sprite_sheet.height}px")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Create OpenHistorical Map sprite set from images in a directory',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_sprite_set.py ./icons
  python create_sprite_set.py ./markers my-markers
  python create_sprite_set.py ./icons sprites --pixel-ratio 2
  python create_sprite_set.py ./icons sprites --max-size 4096
        """
    )
    
    parser.add_argument('input_directory', 
                        help='Directory containing images to package')
    parser.add_argument('output_name', 
                        nargs='?', 
                        default='sprites',
                        help='Name for the sprite set (default: sprites)')
    parser.add_argument('--pixel-ratio', 
                        type=int, 
                        default=1,
                        choices=[1, 2, 4],
                        help='Pixel ratio for the sprite (default: 1)')
    parser.add_argument('--max-size', 
                        type=int, 
                        default=2048,
                        help='Maximum dimension for sprite sheet (default: 2048)')
    
    args = parser.parse_args()
    
    # Validate input directory
    input_dir = Path(args.input_directory)
    if not input_dir.exists():
        print(f"Error: Directory '{input_dir}' does not exist!")
        sys.exit(1)
    
    if not input_dir.is_dir():
        print(f"Error: '{input_dir}' is not a directory!")
        sys.exit(1)
    
    # Create sprite set
    success = create_sprite_set(
        input_dir=input_dir,
        output_name=args.output_name,
        pixel_ratio=args.pixel_ratio,
        max_size=args.max_size
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
