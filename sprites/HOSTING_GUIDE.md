# How to Host and Use Your Sprite Set

## Overview

After generating your sprite set (PNG + JSON files), you need to host them somewhere accessible and reference them in your map style configuration. OpenHistorical Map uses MapLibre GL, which is compatible with the Mapbox sprite format.

## Hosting Options

### 1. Self-Hosting on Your Own Server/CDN

The most common approach is to upload your sprite files to your own web server or CDN.

**Required Files:**
```
/path/to/sprites/
├── sprites.png        # Standard resolution sprite sheet
├── sprites@2x.png     # High-DPI/retina sprite sheet (optional but recommended)
└── sprites.json       # Metadata for both resolutions
```

**Steps:**
1. Upload both the `.png` and `.json` files to a publicly accessible directory on your server
2. Ensure the files are served with appropriate CORS headers if your map is on a different domain
3. Note the base URL (without file extensions)

**Example URLs:**
- `https://yourdomain.com/sprites/sprites.png`
- `https://yourdomain.com/sprites/sprites.json`
- `https://yourdomain.com/sprites/sprites@2x.png`

### 2. Cloud Storage (S3, Google Cloud Storage, Azure Blob)

Upload your sprite files to cloud storage with public read access.

**AWS S3 Example:**
```bash
# Upload files
aws s3 cp sprites.png s3://your-bucket/sprites/sprites.png --acl public-read
aws s3 cp sprites@2x.png s3://your-bucket/sprites/sprites@2x.png --acl public-read
aws s3 cp sprites.json s3://your-bucket/sprites/sprites.json --acl public-read

# Your base URL will be:
# https://your-bucket.s3.amazonaws.com/sprites/sprites
```

**Important:** Configure CORS on your bucket:
```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET"],
    "AllowedOrigins": ["*"],
    "ExposeHeaders": []
  }
]
```

### 3. GitHub Pages (Free Option)

Great for open-source projects or testing.

**Steps:**
1. Create a GitHub repository
2. Add your sprite files to a directory (e.g., `/sprites/`)
3. Enable GitHub Pages in repository settings
4. Access via: `https://username.github.io/repo-name/sprites/sprites`

### 4. CDN Services

**Cloudflare CDN:**
- Upload to R2 (Cloudflare's object storage)
- Enable public access
- Use the R2 public URL

**Netlify:**
- Deploy your sprites as part of a static site
- Automatic CDN distribution

**jsDelivr (for GitHub repos):**
- `https://cdn.jsdelivr.net/gh/username/repo@branch/sprites/sprites.png`

## Using Sprites in Your Map Style

### MapLibre GL / OpenHistorical Map

Once hosted, reference your sprites in your map's style JSON:

```json
{
  "version": 8,
  "name": "My Historical Map Style",
  "sprite": "https://yourdomain.com/sprites/sprites",
  "glyphs": "https://tiles.openhistoricalmap.org/fonts/{fontstack}/{range}.pbf",
  "sources": {
    "openmaptiles": {
      "type": "vector",
      "url": "https://tiles.openhistoricalmap.org/omtiles.json"
    }
  },
  "layers": [
    {
      "id": "poi-labels",
      "type": "symbol",
      "source": "openmaptiles",
      "source-layer": "poi",
      "layout": {
        "icon-image": "park",
        "icon-size": 1,
        "text-field": "{name}",
        "text-offset": [0, 1.5]
      }
    }
  ]
}
```

**Key Points:**
- The `sprite` value is the base URL **without** file extensions
- MapLibre automatically appends `.png`, `.json`, and `@2x.png` as needed
- On high-DPI displays, it requests `sprites@2x.png` automatically

### Multiple Sprite Sets

You can load multiple sprite sets:

```json
{
  "sprite": [
    {
      "id": "default",
      "url": "https://yourdomain.com/sprites/sprites"
    },
    {
      "id": "custom-markers",
      "url": "https://yourdomain.com/markers/historical-markers"
    }
  ]
}
```

Then reference sprites with their ID prefix:
```json
{
  "layout": {
    "icon-image": "custom-markers/location-marker"
  }
}
```

## Using Sprites in Map Code

### JavaScript (MapLibre GL)

```javascript
const map = new maplibregl.Map({
  container: 'map',
  style: {
    version: 8,
    sprite: 'https://yourdomain.com/sprites/sprites',
    sources: {
      // your sources
    },
    layers: [
      {
        id: 'historical-markers',
        type: 'symbol',
        source: 'historical-points',
        layout: {
          'icon-image': 'location-marker',  // name from your sprite JSON
          'icon-size': 1.5,
          'icon-allow-overlap': true
        }
      }
    ]
  }
});

// Or add a sprite dynamically
map.on('load', () => {
  map.addSprite('custom', 'https://yourdomain.com/sprites/sprites');
});
```

### Programmatically Adding Custom Icons

If you need to add individual icons dynamically (not from a sprite sheet):

```javascript
map.on('load', () => {
  map.loadImage('https://yourdomain.com/icon.png', (error, image) => {
    if (error) throw error;
    map.addImage('custom-icon', image);
  });
});
```

## CORS Configuration

**Critical:** Your sprite files must be served with proper CORS headers, especially if your map is hosted on a different domain.

### Apache (.htaccess)
```apache
<FilesMatch "\.(png|json)$">
  Header set Access-Control-Allow-Origin "*"
</FilesMatch>
```

### Nginx
```nginx
location /sprites/ {
    add_header Access-Control-Allow-Origin *;
    add_header Access-Control-Allow-Methods 'GET';
}
```

### Node.js/Express
```javascript
app.use('/sprites', (req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  next();
});
```

## Best Practices

1. **Use a CDN**: Improves load times globally
2. **Enable Gzip/Brotli**: Compress JSON and PNG files
3. **Set Cache Headers**: Sprites rarely change
   ```
   Cache-Control: public, max-age=31536000
   ```
4. **Always provide @2x**: Essential for retina displays
5. **Keep sprite names short**: Reduces JSON file size
6. **Optimize PNGs**: Use tools like `pngquant` or `optipng`
7. **Version your URLs**: For cache busting when updating sprites
   ```
   https://yourdomain.com/sprites/v2/sprites
   ```

## Testing Your Sprites

### 1. Direct URL Test
Open these URLs in your browser:
- `https://yourdomain.com/sprites/sprites.json`
- `https://yourdomain.com/sprites/sprites.png`

### 2. CORS Test
```javascript
fetch('https://yourdomain.com/sprites/sprites.json')
  .then(r => r.json())
  .then(data => console.log('Sprites loaded:', data))
  .catch(err => console.error('CORS or loading error:', err));
```

### 3. Test in Map
Create a simple HTML file:
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://unpkg.com/maplibre-gl/dist/maplibre-gl.js"></script>
  <link href="https://unpkg.com/maplibre-gl/dist/maplibre-gl.css" rel="stylesheet" />
  <style>
    #map { position: absolute; top: 0; bottom: 0; width: 100%; }
  </style>
</head>
<body>
  <div id="map"></div>
  <script>
    const map = new maplibregl.Map({
      container: 'map',
      style: {
        version: 8,
        sprite: 'https://yourdomain.com/sprites/sprites',
        sources: {
          'test': {
            'type': 'geojson',
            'data': {
              'type': 'Feature',
              'geometry': {
                'type': 'Point',
                'coordinates': [0, 0]
              }
            }
          }
        },
        layers: [{
          'id': 'test-icon',
          'type': 'symbol',
          'source': 'test',
          'layout': {
            'icon-image': 'location-marker',  // your sprite name
            'icon-size': 2
          }
        }]
      },
      center: [0, 0],
      zoom: 2
    });
  </script>
</body>
</html>
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Icons not appearing | Check browser console for CORS errors |
| 404 errors | Verify file URLs and paths are correct |
| Wrong icon showing | Check sprite name matches JSON key exactly |
| Blurry icons on retina | Ensure @2x files are present and properly named |
| Slow loading | Use CDN and enable compression |

## OpenHistorical Map Specific Notes

When contributing to OHM or using OHM's infrastructure:

1. **Official OHM sprites** are hosted at: `https://tiles.openhistoricalmap.org/sprites/`
2. For custom styles, host your own sprites separately
3. OHM follows the same MapLibre sprite specification
4. Use the [OHM style repository](https://github.com/OpenHistoricalMap/map-styles) as reference

## Example Complete Setup

```bash
# 1. Generate sprites
python create_sprite_set.py ./icons historical-markers --pixel-ratio 2

# 2. Upload to server
scp historical-markers.png user@server:/var/www/html/sprites/
scp historical-markers@2x.png user@server:/var/www/html/sprites/
scp historical-markers.json user@server:/var/www/html/sprites/

# 3. Use in style JSON
# "sprite": "https://yourserver.com/sprites/historical-markers"
```

## Resources

- [MapLibre Sprite Specification](https://maplibre.org/maplibre-style-spec/sprite/)
- [Mapbox Sprite Documentation](https://docs.mapbox.com/style-spec/reference/sprite/)
- [OpenHistorical Map](https://www.openhistoricalmap.org/)
- [Spreet - Alternative sprite generator](https://github.com/flother/spreet)
- [Spritezero - MapBox's sprite tool](https://github.com/mapbox/spritezero)
