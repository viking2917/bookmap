# OpenHistorical Map Sprite Set Generator

A Python script that packages all images in a directory into a sprite sheet with accompanying JSON metadata, compatible with OpenHistorical Map format.

## Features

- ✅ Automatically packs images into an optimized sprite sheet
- ✅ Generates JSON metadata with sprite coordinates
- ✅ Supports multiple pixel ratios (@1x, @2x, @4x)
- ✅ Handles PNG, JPG, GIF, BMP, and WebP formats
- ✅ Efficient shelf-packing algorithm
- ✅ Configurable sprite sheet dimensions

## Requirements

```bash
pip install Pillow
```

## Usage

### Basic Usage

```bash
# Create sprite set from images in a directory
python create_sprite_set.py ./icons

# This will create:
# - icons/sprites.png (the sprite sheet)
# - icons/sprites.json (the metadata)
```

### Custom Output Name

```bash
python create_sprite_set.py ./markers my-markers

# Creates:
# - markers/my-markers.png
# - markers/my-markers.json
```

### High DPI / Retina Support

```bash
# Create @2x sprite for retina displays
python create_sprite_set.py ./icons sprites --pixel-ratio 2

# Creates:
# - icons/sprites@2x.png
# - icons/sprites.json (with pixelRatio: 2)
```

### Large Sprite Sheets

```bash
# Increase maximum sprite sheet size to 4096x4096
python create_sprite_set.py ./icons sprites --max-size 4096
```

### Complete Example

```bash
python create_sprite_set.py ./map-icons historical-markers --pixel-ratio 2 --max-size 4096
```

## Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `input_directory` | Directory containing images (required) | - |
| `output_name` | Name for sprite set files | `sprites` |
| `--pixel-ratio` | Pixel ratio (1, 2, or 4) | `1` |
| `--max-size` | Maximum sprite sheet dimension | `2048` |

## Output Format

### Sprite Sheet (PNG)
A single PNG image containing all sprites packed efficiently with transparent background.

### Metadata (JSON)
JSON file with sprite coordinates and dimensions:

```json
{
  "airport": {
    "x": 2,
    "y": 2,
    "width": 24,
    "height": 24,
    "pixelRatio": 1
  },
  "building": {
    "x": 28,
    "y": 2,
    "width": 24,
    "height": 24,
    "pixelRatio": 1
  }
}
```

## OpenHistorical Map Integration

To use the generated sprite set with OpenHistorical Map:

```javascript
map.addSprite('my-sprites', '/path/to/sprites.json');

// Then use sprites in your style
{
  "id": "poi-layer",
  "type": "symbol",
  "source": "poi-source",
  "layout": {
    "icon-image": "airport",
    "icon-size": 1
  }
}
```

## Supported Image Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- BMP (.bmp)
- WebP (.webp)

All images are automatically converted to RGBA for consistent sprite sheet generation.

## Tips

1. **Image naming**: The filename (without extension) becomes the sprite ID
2. **Image size**: Keep individual sprites reasonably sized (e.g., 16x16 to 128x128)
3. **Transparency**: PNG images with transparency are fully supported
4. **Optimization**: The script automatically optimizes the PNG output
5. **Retina displays**: Use `--pixel-ratio 2` for high-DPI screens

## Example Directory Structure

Before:
```
icons/
├── airport.png
├── building.png
├── park.png
└── school.png
```

After running `python create_sprite_set.py ./icons`:
```
icons/
├── airport.png
├── building.png
├── park.png
├── school.png
├── sprites.png      ← Generated sprite sheet
└── sprites.json     ← Generated metadata
```

## Troubleshooting

### "Cannot fit all images within sprite sheet"
- Increase `--max-size` parameter
- Reduce the size of individual images
- Split images into multiple sprite sets

### "No valid images found in directory"
- Verify directory path is correct
- Check that images have supported file extensions
- Ensure files are not corrupted

## License

This script is provided as-is for creating sprite sets compatible with OpenHistorical Map.
