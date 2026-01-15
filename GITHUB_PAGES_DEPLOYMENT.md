# Deploying Sprites to GitHub Pages

This guide walks you through setting up and deploying your sprite files to GitHub Pages from scratch.

## Quick Start (Complete Workflow)

```bash
# 1. Create a new repository on GitHub (via web interface)
#    Name it something like "map-sprites" or "ohm-sprites"

# 2. Clone the repository locally
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

# 3. Create sprites directory
mkdir sprites

# 4. Generate your sprite files (place them in sprites/)
python create_sprite_set.py ./icons sprites --pixel-ratio 2
mv sprites.png sprites/
mv sprites@2x.png sprites/
mv sprites.json sprites/

# 5. Add and commit
git add sprites/
git commit -m "Add sprite set"

# 6. Push to GitHub
git push origin main

# 7. Enable GitHub Pages (see below)
```

## Method 1: Using Main Branch (Simplest)

### Step 1: Create Repository Structure

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/map-sprites.git
cd map-sprites

# Create directory structure
mkdir -p sprites
```

### Step 2: Add Your Sprite Files

```bash
# Copy or generate sprites into the sprites/ directory
cp /path/to/sprites.png sprites/
cp /path/to/sprites@2x.png sprites/
cp /path/to/sprites.json sprites/

# Or generate directly into the directory
python create_sprite_set.py ./my-icons sprites --pixel-ratio 2
mv sprites.* sprites/
```

### Step 3: Create index.html (Optional but Recommended)

```bash
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Map Sprites</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 50px auto; 
            padding: 20px;
        }
        .sprite-info {
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        code {
            background: #333;
            color: #fff;
            padding: 2px 6px;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <h1>Map Sprite Set</h1>
    <p>Available sprites for use in maps.</p>
    
    <div class="sprite-info">
        <h2>Usage</h2>
        <p>Base URL: <code id="baseUrl"></code></p>
        <p>In your map style JSON:</p>
        <pre><code>{
  "sprite": "<span id="spriteUrl"></span>"
}</code></pre>
    </div>

    <h2>Files</h2>
    <ul>
        <li><a href="sprites/sprites.json">sprites.json</a> - Sprite metadata</li>
        <li><a href="sprites/sprites.png">sprites.png</a> - Sprite image (1x)</li>
        <li><a href="sprites/sprites@2x.png">sprites@2x.png</a> - Sprite image (2x)</li>
    </ul>

    <script>
        const baseUrl = window.location.origin + window.location.pathname.replace(/\/$/, '');
        const spriteUrl = baseUrl + '/sprites/sprites';
        document.getElementById('baseUrl').textContent = spriteUrl;
        document.getElementById('spriteUrl').textContent = spriteUrl;
    </script>
</body>
</html>
EOF
```

### Step 4: Commit and Push

```bash
git add .
git commit -m "Add sprite files and index page"
git push origin main
```

### Step 5: Enable GitHub Pages

**Via GitHub Website:**
1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll down to **Pages** section (in left sidebar under "Code and automation")
4. Under **Source**, select:
   - **Branch:** `main` 
   - **Folder:** `/ (root)`
5. Click **Save**

**GitHub will show you the URL where your site is published:**
```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/
```

### Step 6: Access Your Sprites

After a few minutes, your sprites will be available at:
```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/sprites/sprites
```

Use this URL in your map style:
```json
{
  "sprite": "https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/sprites/sprites"
}
```

## Method 2: Using gh-pages Branch (Alternative)

This method keeps your sprites separate from your main code branch.

### Initial Setup

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/map-sprites.git
cd map-sprites

# Create and switch to gh-pages branch
git checkout --orphan gh-pages

# Remove any existing files
git rm -rf .

# Add sprites
mkdir sprites
cp /path/to/sprites.* sprites/

# Create simple index
echo "<h1>Map Sprites</h1><p>Sprites available at /sprites/sprites</p>" > index.html

# Commit and push
git add .
git commit -m "Initialize gh-pages with sprites"
git push origin gh-pages
```

### Enable GitHub Pages
1. Go to repository **Settings** → **Pages**
2. Select **Branch:** `gh-pages`
3. **Folder:** `/ (root)`
4. Click **Save**

### Updating Sprites

```bash
# Switch to gh-pages branch
git checkout gh-pages

# Update sprite files
cp /path/to/new-sprites.* sprites/

# Commit and push
git add sprites/
git commit -m "Update sprites"
git push origin gh-pages
```

## Method 3: Using GitHub Actions (Automated)

Automatically deploy when you push to main.

### Step 1: Create Directory Structure

```bash
mkdir -p .github/workflows
mkdir sprites-source
```

### Step 2: Create Workflow File

```bash
cat > .github/workflows/deploy-sprites.yml << 'EOF'
name: Deploy Sprites to GitHub Pages

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install Pillow

      - name: Generate sprites
        run: |
          mkdir -p _site/sprites
          python create_sprite_set.py sprites-source sprites --pixel-ratio 2
          mv sprites.* _site/sprites/
          
      - name: Create index page
        run: |
          cat > _site/index.html << 'HTML'
          <!DOCTYPE html>
          <html>
          <head><title>Map Sprites</title></head>
          <body>
            <h1>Map Sprites</h1>
            <p>Sprite URL: <code id="url"></code></p>
            <ul>
              <li><a href="sprites/sprites.json">sprites.json</a></li>
              <li><a href="sprites/sprites.png">sprites.png</a></li>
              <li><a href="sprites/sprites@2x.png">sprites@2x.png</a></li>
            </ul>
            <script>
              document.getElementById('url').textContent = 
                window.location.origin + window.location.pathname + 'sprites/sprites';
            </script>
          </body>
          </html>
          HTML

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '_site'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
EOF
```

### Step 3: Add Your Files

```bash
# Add sprite source images
cp /path/to/icons/* sprites-source/

# Add the sprite generator script
cp create_sprite_set.py .

# Commit everything
git add .
git commit -m "Setup automated sprite deployment"
git push origin main
```

### Step 4: Enable GitHub Pages
1. Go to **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. The workflow will run automatically on push

## Updating Your Sprites

### For Method 1 or 2 (Manual):

```bash
# Update sprites
python create_sprite_set.py ./updated-icons sprites --pixel-ratio 2

# Move to sprites directory
mv sprites.* sprites/

# Commit and push
git add sprites/
git commit -m "Update sprite set"
git push origin main  # or gh-pages
```

### For Method 3 (Automated):

```bash
# Just update source images
cp /path/to/new-icons/* sprites-source/

# Commit and push - sprites regenerate automatically
git add sprites-source/
git commit -m "Update source icons"
git push origin main
```

## Verification

After deployment (usually 1-5 minutes), verify your sprites are accessible:

```bash
# Check JSON metadata
curl https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/sprites/sprites.json

# Check if images load
curl -I https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/sprites/sprites.png
curl -I https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/sprites/sprites@2x.png
```

Or open in browser:
```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/sprites/sprites.json
```

## Testing in a Map

Create a test HTML file:

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://unpkg.com/maplibre-gl/dist/maplibre-gl.js"></script>
  <link href="https://unpkg.com/maplibre-gl/dist/maplibre-gl.css" rel="stylesheet" />
  <style>#map { position: absolute; top: 0; bottom: 0; width: 100%; }</style>
</head>
<body>
  <div id="map"></div>
  <script>
    const map = new maplibregl.Map({
      container: 'map',
      style: {
        version: 8,
        sprite: 'https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/sprites/sprites',
        sources: {
          'test': {
            type: 'geojson',
            data: {
              type: 'Feature',
              geometry: { type: 'Point', coordinates: [0, 0] }
            }
          }
        },
        layers: [{
          id: 'test',
          type: 'symbol',
          source: 'test',
          layout: { 
            'icon-image': 'park',  // Replace with your sprite name
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
| 404 on sprite files | Wait 2-5 minutes after push for GitHub Pages to build |
| Page not updating | Clear browser cache or add `?v=timestamp` to URL |
| Workflow not running | Check **Actions** tab for errors |
| Wrong URL | Use the exact URL shown in Settings → Pages |

## Custom Domain (Optional)

To use a custom domain like `sprites.yourdomain.com`:

1. Add a `CNAME` file to your repository:
   ```bash
   echo "sprites.yourdomain.com" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. Add DNS record:
   ```
   Type: CNAME
   Name: sprites
   Value: YOUR_USERNAME.github.io
   ```

3. In GitHub Settings → Pages, enter your custom domain

## Best Practices

1. **Use descriptive commit messages** for sprite updates
2. **Tag releases** for version tracking:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. **Keep source images** in a separate directory for regeneration
4. **Add a README** documenting available sprites
5. **Use GitHub releases** to attach downloadable sprite sets

## Example Repository Structure

```
map-sprites/
├── .github/
│   └── workflows/
│       └── deploy-sprites.yml
├── sprites/
│   ├── sprites.json
│   ├── sprites.png
│   └── sprites@2x.png
├── sprites-source/          # Optional: source images
│   ├── park.png
│   ├── building.png
│   └── ...
├── create_sprite_set.py
├── index.html
├── README.md
└── CNAME                    # Optional: for custom domain
```

## Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions for Pages](https://github.com/actions/deploy-pages)
- [Using a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
