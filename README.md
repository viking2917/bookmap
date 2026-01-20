# Open Historical Map style


I wanted to make maps that look like the maps you see in history or historical fiction books, so 
I went on map safari to learn about map display. In particular, I explored using MapLibre to generate map displays 
in a style like what is seen in books. 

ChatGPT summarizes things more quickly than I can:

> OpenStreetMap (OSM) is a global, community-maintained open dataset of geographic features—roads, buildings, boundaries, places, and more—that serves as a foundational source for many modern maps. Tools like OpenMapTiles transform raw OSM data into performant vector tiles, which can then be styled and rendered in the browser or native apps using MapLibre GL, an open-source map rendering engine derived from Mapbox GL. MapTiler builds on this ecosystem by providing hosted vector and raster tiles, terrain, hillshade, and style tools that are compatible with MapLibre, making it easier to deploy production maps without running your own tile infrastructure. Together with related standards and technologies—such as vector tiles (MVT), GeoJSON, sprites, glyphs, and style specifications—this stack enables highly customizable, scalable, and license-friendly web mapping, giving developers full control over cartography while avoiding proprietary lock-in.

Some nomenclature: *tiles* are small, fixed-size chunks of geographic data—raster images or vector features—served at multiple zoom levels to make maps fast and scalable, while *sprites* are compact image sheets that bundle many small icons and patterns (like markers, shields, or line textures) into a single file to reduce network requests. Vector tiles carry geometry and attributes that are styled client-side, enabling dynamic cartography, whereas sprites provide the visual symbols referenced by a map style for consistent rendering.

This repo is the result of my explorations.

I created a Maplibre "style" that renders somewhat like the examples I mentioned. I've created two styles, the first is a simple style ([bookmap.json](bookmap.json)) that renders key elements: the land, a "hillside shading" (what I used to call Google Maps Terrain), a background "paper" image to give the land a vintage look, and a "land gradient" from MapTiler that gives some color and shading to the ocean, and coastlines in particular. I wanted to create a coastal hatching pattern, but that seems a bridge too far for me at the moment. 

Along the way, I discovered Open Historical Maps, a super cool project that links historical geographical data to the maps. (I.e what were the geographic boundaries of the Holy Roman Empire in 1187AD?). I created [another style](bookmap_openhistorical.json) another style that shows major kingdoms and their boundaries, and my example map is set during the year 1187AD as I have been studying the Third Crusade which began around then. 

I then created two map examples that show these two styles rendered, along with custom POI markers that again emulate what you might see in a "bookish" map. 

Click [this link](index.html) to browse around live examples.

Much of this code was created with Claude.AI. Caveat emptor.

## Live example maps

* [Simple map](map.html) - shows the base style of ocean gradient, terrain, and paper texture background.
* [Historical map](map_openhistorical.html) - the base map, plus inclusion of Open Historical Map kingdom and kingdom boundary data. Year set to 1187 AD.


Open the example maps to see the results. The map pages allow you to

1. **Export Map** to save the map image to a file (in case you want to include in a blog post!)
2. **Set POI** to change the POI data to your own locations. 
   
The format for POI entry is an array of lat/lon/name/description entries:

```
[
  [51.5074, -0.1278, "London", "London, England"],
  [48.8566, 2.3522, "Paris", "Paris, France"],
]
```

## Inspirations

I looked at a number of interesting articles about map styles, vintage map styles in particular. I found these articles particularly interesting and helpful. 

https://medium.com/greeninfo-network/how-to-make-a-historic-style-444af3f2b6fc  
https://medium.com/greeninfo-network/the-making-of-openhistoricalmaps-japanese-scroll-map-style-350400447c42  
https://blog.mapbox.com/designing-the-vintage-style-in-mapbox-studio-9da4aa2a627f  
https://kmalexander.com/2019/07/31/tutorial-creating-18th-century-coastlines-for-fantasy-maps/  
https://andywoodruff.com/posts/2024/qgis-hand-drawn-maps/  
https://docs.maptiler.com/guides/map-design/land-gradient/  
https://www.mapbox.com/blog/new-bathymetry-tileset-and-style-for-marine-maps  
https://www.mapeffects.co/tutorials/ocean-hatching  

## Process notes

Maputnik is a tool for editing map styles. Go to [Maputnik](https://maplibre.org/maputnik), then click **Open**, which will let you pick some default styles. Or, hit **Code Editor** and paste in the contents of my bookmap.json file to see (and edit) my book map style.

You can learn more about how to code with Open Historical Maps [here](https://wiki.openstreetmap.org/wiki/OpenHistoricalMap/Reuse).

The code for this repo (including the map pages, the styles, and the sprites) are hosted on github pages. 

As a courtesy you should get your own MapTiler API key and replace the key used in bookmap.json.

I had to enable maplibregl dates to for the date-setting code to work in map.html (https://github.com/OpenHistoricalMap/maplibre-gl-dates/)

## Tiles

My styles use a few different tiles, which you can see referenced in the style files.

As mentioned, get your own API key, please don't use mine.

* maptiler-hillshade: used to show terrain
* land: a maptiler set used to draw lines around coastlines
* land-gradient: a maptiler tile set used to create a dark gradient around coastlines, extending out into oceans
* osm: an Open Historical Map tileset used to render historical kingdom names and boundaries (only used by map_openhistorical.html)

## Sprites

I have a small script that takes all the images in sprites/spriteimages and bundles them into a maplibre-gl format sprite file. It is invoked with `npm run sprites`. The results are hosted on github pages and referenced by the styles.

## Credits

I can no longer find the source of the paper texture I used, but it was open source via pixabay.