# Open Historical Map style

style was
  "sprite": "https://www.openhistoricalmap.org/map-styles/woodblock/woodblock_spritesheet",


## code

https://wiki.openstreetmap.org/wiki/OpenHistoricalMap/Reuse

https://github.com/OpenHistoricalMap/maplibre-gl-dates/

## process

went to maptiler cloud, I think I started with Backdrop v4? (no, though it is interesting)

I used Maputnik, Open, Positron, and customized from there.

Inspired by 


https://blog.greeninfo.org/how-to-make-a-historic-style-444af3f2b6fc

https://blog.greeninfo.org/how-to-recreate-a-map-style-1d288ed8d398

https://kmalexander.com/2019/07/31/tutorial-creating-18th-century-coastlines-for-fantasy-maps/

https://blog.mapbox.com/designing-the-vintage-style-in-mapbox-studio-9da4aa2a627f

https://www.mapbox.com/blog/new-bathymetry-tileset-and-style-for-marine-maps



questions
show historical state boundaries


## the stack

maplibregl

open historical map

maptiler

maputnik

map tiles & sources



get the hillside layer


sea of galilee
    {
      "id": "water_areas_ne",
      "type": "fill",
      "source": "ne",
      "source-layer": "water_areas",
      "minzoom": 0,
      "maxzoom": 8,
      "layout": {"visibility": "visible"},
      "paint": {
        "fill-color": [
          "interpolate",
          ["linear"],
          ["zoom"],
          0,
          "rgba(185, 228, 228, 1)",
          10,
          "rgba(126, 218, 218, 1)"
        ]
      }
    },

    rivers
     {
      "id": "water_lines_river",
      "type": "line",
      "source": "osm",
      "source-layer": "water_lines",
      "minzoom": 8,
      "maxzoom": 24,
      "filter": ["==", ["get", "type"], "river"],
      "paint": {
        "line-color": [
          "interpolate",
          ["linear"],
          ["zoom"],
          0,
          "#B9E4E4",
          10,
          "rgba(126, 218, 218, 1)"
        ],
        "line-width": [
          "interpolate",
          ["linear"],
          ["zoom"],
          8,
          1,
          13,
          2,
          14,
          5,
          20,
          12
        ]
      }
    },


    a good one for names of countries
    admin_country_lines_z10

    this no: admin_country_lines_z10_case

    no: county_labels_z11_admin_6_centroids

    for labels: country_points_labels_cen

  {
      "id": "country_points_labels_cen",
      "type": "symbol",
      "source": "osm",
      "source-layer": "land_ohm_centroids",
      "maxzoom": 12,
      "filter": [
        "all",
        ["==", ["get", "type"], "administrative"],
        ["==", ["get", "admin_level"], 2]
      ],
      "layout": {
        "symbol-sort-key": ["get", "area_km2"],
        "text-line-height": 1,
        "text-size": [
          "interpolate",
          ["linear"],
          ["zoom"],
          0,
          8,
          3,
          12,
          6,
          20,
          10,
          22
        ],
        "symbol-avoid-edges": false,
        "text-font": ["OpenHistorical Bold"],
        "symbol-placement": "point",
        "text-justify": "center",
        "visibility": "visible",
        "text-field": ["get", "name"],
        "text-max-width": 7
      },
      "paint": {
        "text-color": [
          "interpolate",
          ["linear"],
          ["zoom"],
          0,
          "#495049",
          5,
          "#6d786d"
        ],
        "text-halo-width": 1.5,
        "text-halo-color": [
          "interpolate",
          ["linear"],
          ["zoom"],
          0,
          "rgba(252, 255, 254, 0.75)",
          3,
          "rgba(240, 244, 216, 1)",
          5,
          "rgba(246,247,227, 1)",
          7,
          "rgba(255, 255, 255, 1)"
        ],
        "text-halo-blur": 1,
        "text-opacity": 1,
        "text-translate-anchor": "map"
      }
    },
    {
      "id": "country_points_labels",
      "type": "symbol",
      "source": "osm",
      "source-layer": "place_points_centroids",
      "minzoom": 0,
      "maxzoom": 12,
      "filter": ["==", ["get", "type"], "country"],
      "layout": {
        "text-line-height": 1,
        "text-size": [
          "interpolate",
          ["linear"],
          ["zoom"],
          0,
          8,
          3,
          12,
          6,
          20,
          10,
          22
        ],
        "symbol-avoid-edges": false,
        "text-font": ["OpenHistorical Bold"],
        "symbol-placement": "point",
        "text-justify": "center",
        "visibility": "visible",
        "text-field": ["get", "name"],
        "text-max-width": 7
      },
      "paint": {
        "text-color": [
          "interpolate",
          ["linear"],
          ["zoom"],
          0,
          "#495049",
          5,
          "#6d786d"
        ],
        "text-halo-width": 1.5,
        "text-halo-color": [
          "interpolate",
          ["linear"],
          ["zoom"],
          0,
          "rgba(252, 255, 254, 0.75)",
          3,
          "rgba(240, 244, 216, 1)",
          5,
          "rgba(246,247,227, 1)",
          7,
          "rgba(255, 255, 255, 1)"
        ],
        "text-halo-blur": 1,
        "text-opacity": 1,
        "text-translate-anchor": "map"
      }
    }


        {
      "id": "state_points_labels_centroids",
      "type": "symbol",
      "source": "osm",
      "source-layer": "land_ohm_centroids",
      "minzoom": 5,
      "maxzoom": 20,
      "filter": [
        "all",
        [
          "==",
          ["get", "type"],
          "administrative"
        ],
        [
          "==",
          ["get", "admin_level"],
          4
        ]
      ],
      "layout": {
        "text-line-height": 1,
        "text-size": [
          "interpolate",
          ["linear"],
          ["zoom"],
          3,
          9,
          6,
          15,
          10,
          18
        ],
        "symbol-avoid-edges": true,
        "text-transform": "uppercase",
        "symbol-spacing": 25,
        "text-font": ["OpenHistorical"],
        "symbol-placement": "point",
        "visibility": "visible",
        "text-field": ["get", "name"]
      },
      "paint": {
        "text-color": [
          "interpolate",
          ["linear"],
          ["zoom"],
          6,
          "rgba(110, 133, 123, 1)"
        ],
        "text-halo-width": 2,
        "text-halo-blur": 1,
        "text-halo-color": [
          "interpolate",
          ["linear"],
          ["zoom"],
          0,
          "rgba(252, 255, 254, 0.75)",
          3,
          "rgba(240, 244, 216, 1)",
          5,
          "rgba(246,247,227, 1)",
          7,
          "rgba(255, 255, 255, 1)"
        ],
        "text-translate-anchor": "map",
        "icon-translate-anchor": "map"
      }
    },
    {
      "id": "state_points_labels",
      "type": "symbol",
      "source": "osm",
      "source-layer": "place_points_centroids",
      "minzoom": 5,
      "maxzoom": 20,
      "filter": [
        "in",
        ["get", "type"],
        [
          "literal",
          ["state", "territory"]
        ]
      ],
      "layout": {
        "text-line-height": 1,
        "text-size": [
          "interpolate",
          ["linear"],
          ["zoom"],
          3,
          9,
          6,
          15,
          10,
          18
        ],
        "symbol-avoid-edges": true,
        "text-transform": "uppercase",
        "symbol-spacing": 25,
        "text-font": ["OpenHistorical"],
        "symbol-placement": "point",
        "visibility": "visible",
        "text-field": ["get", "name"]
      },
      "paint": {
        "text-color": [
          "interpolate",
          ["linear"],
          ["zoom"],
          6,
          "rgba(110, 133, 123, 1)"
        ],
        "text-halo-width": 2,
        "text-halo-blur": 1,
        "text-halo-color": [
          "interpolate",
          ["linear"],
          ["zoom"],
          0,
          "rgba(252, 255, 254, 0.75)",
          3,
          "rgba(240, 244, 216, 1)",
          5,
          "rgba(246,247,227, 1)",
          7,
          "rgba(255,255,255, 1)"
        ],
        "text-translate-anchor": "map",
        "icon-translate-anchor": "map"
      }
    },


    country lines
     {
      "id": "admin_admin3",
      "type": "line",
      "source": "osm",
      "source-layer": "land_ohm_lines",
      "minzoom": 5,
      "maxzoom": 20,
      "filter": ["==", ["get", "admin_level"], 3],
      "layout": {
        "visibility": "visible",
        "line-cap": "square",
        "line-join": "round"
      },
      "paint": {
        "line-color": "rgba(168, 193, 183, 1)",
        "line-width": ["interpolate", ["linear"], ["zoom"], 6, 0.75, 12, 2]
      }
    },
    {
      "id": "admin_country_lines_z10_case",
      "type": "line",
      "source": "osm",
      "source-layer": "land_ohm_lines",
      "minzoom": 0,
      "maxzoom": 20,
      "filter": ["in", ["get", "admin_level"], ["literal", [1, 2]]],
      "layout": {
        "visibility": "visible",
        "line-cap": "square",
        "line-join": "round"
      },
      "paint": {
        "line-color": [
          "interpolate",
          ["linear"],
          ["zoom"],
          4,
          "rgba(133, 147, 156, 0.1)",
          6,
          "#e3e6e8",
          9,
          "#f1f3f4"
        ],
        "line-width": ["interpolate", ["linear"], ["zoom"], 6, 0, 12, 7, 15, 11]
      }
    },
    {
      "id": "admin_country_lines_z10",
      "type": "line",
      "source": "osm",
      "source-layer": "land_ohm_lines",
      "minzoom": 0,
      "maxzoom": 20,
      "filter": ["in", ["get", "admin_level"], ["literal", [1, 2]]],
      "layout": {
        "visibility": "visible",
        "line-cap": "square",
        "line-join": "round"
      },
      "paint": {
        "line-color": [
          "interpolate",
          ["linear"],
          ["zoom"],
          4,
          "rgba(126, 144, 127, 1)",
          6,
          "rgba(147, 171, 148, 1)",
          8,
          "rgba(177, 182, 177, 1)",
          12,
          "rgba(203, 212, 203, 1)"
        ],
        "line-width": [
          "interpolate",
          ["linear"],
          ["zoom"],
          0,
          0.25,
          2,
          0.75,
          4,
          1,
          6,
          2,
          12,
          2.5,
          15,
          4
        ]
      }
    },




    maxbox halo
    {
    "id": "settlement-major-label",
    "type": "symbol",
    "metadata": {
        "mapbox:group": "place labels"
    },
    "source": "composite",
    "source-layer": "place_label",
    "minzoom": 2,
    "maxzoom": 15,
    "filter": [
        "all",
        [
            "<=",
            [
                "get",
                "filterrank"
            ],
            3
        ],
        [
            "match",
            [
                "get",
                "class"
            ],
            [
                "settlement",
                "disputed_settlement"
            ],
            [
                "case",
                [
                    "has",
                    "$localized"
                ],
                true,
                [
                    "match",
                    [
                        "get",
                        "worldview"
                    ],
                    [
                        "all",
                        "US"
                    ],
                    true,
                    false
                ]
            ],
            false
        ],
        [
            "step",
            [
                "zoom"
            ],
            false,
            2,
            [
                "<=",
                [
                    "get",
                    "symbolrank"
                ],
                6
            ],
            4,
            [
                "<",
                [
                    "get",
                    "symbolrank"
                ],
                7
            ],
            6,
            [
                "<",
                [
                    "get",
                    "symbolrank"
                ],
                8
            ],
            7,
            [
                "<",
                [
                    "get",
                    "symbolrank"
                ],
                10
            ],
            10,
            [
                "<",
                [
                    "get",
                    "symbolrank"
                ],
                11
            ],
            11,
            [
                "<",
                [
                    "get",
                    "symbolrank"
                ],
                13
            ],
            12,
            [
                "<",
                [
                    "get",
                    "symbolrank"
                ],
                15
            ],
            13,
            [
                ">=",
                [
                    "get",
                    "symbolrank"
                ],
                11
            ],
            14,
            [
                ">=",
                [
                    "get",
                    "symbolrank"
                ],
                15
            ]
        ],
        [
            "case",
            [
                "<=",
                [
                    "pitch"
                ],
                45
            ],
            true,
            [
                "<=",
                [
                    "distance-from-center"
                ],
                2
            ]
        ]
    ],
    "layout": {
        "visibility": [
            "case",
            [
                "config",
                "showPlaceLabels"
            ],
            "visible",
            "none"
        ],
        "text-line-height": 1.1,
        "text-size": [
            "interpolate",
            [
                "cubic-bezier",
                0.2,
                0,
                0.9,
                1
            ],
            [
                "zoom"
            ],
            3,
            [
                "step",
                [
                    "get",
                    "symbolrank"
                ],
                13,
                6,
                11
            ],
            6,
            [
                "step",
                [
                    "get",
                    "symbolrank"
                ],
                18,
                6,
                16,
                7,
                14
            ],
            8,
            [
                "step",
                [
                    "get",
                    "symbolrank"
                ],
                20,
                9,
                16,
                10,
                14
            ],
            15,
            [
                "step",
                [
                    "get",
                    "symbolrank"
                ],
                24,
                9,
                20,
                12,
                16,
                15,
                14
            ]
        ],
        "text-radial-offset": [
            "step",
            [
                "zoom"
            ],
            [
                "match",
                [
                    "get",
                    "capital"
                ],
                2,
                0.6,
                0.55
            ],
            8,
            0
        ],
        "symbol-sort-key": [
            "get",
            "symbolrank"
        ],
        "icon-image": [
            "let",
            "h_colorPlaceLabels",
            [
                "at",
                0,
                [
                    "to-hsla",
                    [
                        "config",
                        "colorPlaceLabels"
                    ]
                ]
            ],
            "s_colorPlaceLabels",
            [
                "at",
                1,
                [
                    "to-hsla",
                    [
                        "config",
                        "colorPlaceLabels"
                    ]
                ]
            ],
            "l_colorPlaceLabels",
            [
                "at",
                2,
                [
                    "to-hsla",
                    [
                        "config",
                        "colorPlaceLabels"
                    ]
                ]
            ],
            [
                "step",
                [
                    "zoom"
                ],
                [
                    "case",
                    [
                        "==",
                        [
                            "get",
                            "capital"
                        ],
                        2
                    ],
                    [
                        "image",
                        "border-dot-13",
                        {
                            "params": {
                                "color-primary": [
                                    "match",
                                    [
                                        "config",
                                        "lightPreset"
                                    ],
                                    [
                                        "dusk",
                                        "night"
                                    ],
                                    [
                                        "hsl",
                                        [
                                            "var",
                                            "h_colorPlaceLabels"
                                        ],
                                        [
                                            "var",
                                            "s_colorPlaceLabels"
                                        ],
                                        80
                                    ],
                                    [
                                        "config",
                                        "colorPlaceLabels"
                                    ]
                                ],
                                "color-secondary": [
                                    "match",
                                    [
                                        "config",
                                        "lightPreset"
                                    ],
                                    [
                                        "dusk",
                                        "night"
                                    ],
                                    "hsla(0, 0%, 20%, 1)",
                                    [
                                        "step",
                                        [
                                            "var",
                                            "l_colorPlaceLabels"
                                        ],
                                        "hsla(0, 0%, 100%, 1)",
                                        90,
                                        "hsla(0, 0%, 60%, 1)"
                                    ]
                                ]
                            }
                        }
                    ],
                    [
                        "step",
                        [
                            "get",
                            "symbolrank"
                        ],
                        [
                            "image",
                            "dot-11",
                            {
                                "params": {
                                    "color-primary": [
                                        "match",
                                        [
                                            "config",
                                            "lightPreset"
                                        ],
                                        [
                                            "dusk",
                                            "night"
                                        ],
                                        [
                                            "hsl",
                                            [
                                                "var",
                                                "h_colorPlaceLabels"
                                            ],
                                            [
                                                "var",
                                                "s_colorPlaceLabels"
                                            ],
                                            80
                                        ],
                                        [
                                            "config",
                                            "colorPlaceLabels"
                                        ]
                                    ],
                                    "color-secondary": [
                                        "match",
                                        [
                                            "config",
                                            "lightPreset"
                                        ],
                                        [
                                            "dusk",
                                            "night"
                                        ],
                                        "hsla(0, 0%, 20%, 1)",
                                        [
                                            "step",
                                            [
                                                "var",
                                                "l_colorPlaceLabels"
                                            ],
                                            "hsla(0, 0%, 100%, 1)",
                                            90,
                                            "hsla(0, 0%, 60%, 1)"
                                        ]
                                    ]
                                }
                            }
                        ],
                        9,
                        [
                            "image",
                            "dot-10",
                            {
                                "params": {
                                    "color-primary": [
                                        "match",
                                        [
                                            "config",
                                            "lightPreset"
                                        ],
                                        [
                                            "dusk",
                                            "night"
                                        ],
                                        [
                                            "hsl",
                                            [
                                                "var",
                                                "h_colorPlaceLabels"
                                            ],
                                            [
                                                "var",
                                                "s_colorPlaceLabels"
                                            ],
                                            80
                                        ],
                                        [
                                            "config",
                                            "colorPlaceLabels"
                                        ]
                                    ],
                                    "color-secondary": [
                                        "match",
                                        [
                                            "config",
                                            "lightPreset"
                                        ],
                                        [
                                            "dusk",
                                            "night"
                                        ],
                                        "hsla(0, 0%, 20%, 1)",
                                        [
                                            "step",
                                            [
                                                "var",
                                                "l_colorPlaceLabels"
                                            ],
                                            "hsla(0, 0%, 100%, 1)",
                                            90,
                                            "hsla(0, 0%, 60%, 1)"
                                        ]
                                    ]
                                }
                            }
                        ],
                        11,
                        [
                            "image",
                            "dot-9",
                            {
                                "params": {
                                    "color-primary": [
                                        "match",
                                        [
                                            "config",
                                            "lightPreset"
                                        ],
                                        [
                                            "dusk",
                                            "night"
                                        ],
                                        [
                                            "hsl",
                                            [
                                                "var",
                                                "h_colorPlaceLabels"
                                            ],
                                            [
                                                "var",
                                                "s_colorPlaceLabels"
                                            ],
                                            80
                                        ],
                                        [
                                            "config",
                                            "colorPlaceLabels"
                                        ]
                                    ],
                                    "color-secondary": [
                                        "match",
                                        [
                                            "config",
                                            "lightPreset"
                                        ],
                                        [
                                            "dusk",
                                            "night"
                                        ],
                                        "hsla(0, 0%, 20%, 1)",
                                        [
                                            "step",
                                            [
                                                "var",
                                                "l_colorPlaceLabels"
                                            ],
                                            "hsla(0, 0%, 100%, 1)",
                                            90,
                                            "hsla(0, 0%, 60%, 1)"
                                        ]
                                    ]
                                }
                            }
                        ]
                    ]
                ],
                8,
                ""
            ]
        ],
        "text-font": [
            [
                "concat",
                [
                    "config",
                    "font"
                ],
                " Medium"
            ],
            "Arial Unicode MS Bold"
        ],
        "text-justify": [
            "step",
            [
                "zoom"
            ],
            [
                "match",
                [
                    "get",
                    "text_anchor"
                ],
                [
                    "left",
                    "bottom-left",
                    "top-left"
                ],
                "left",
                [
                    "right",
                    "bottom-right",
                    "top-right"
                ],
                "right",
                "center"
            ],
            8,
            "center"
        ],
        "text-anchor": [
            "step",
            [
                "zoom"
            ],
            [
                "get",
                "text_anchor"
            ],
            8,
            "center"
        ],
        "text-field": [
            "coalesce",
            [
                "get",
                "name_en"
            ],
            [
                "get",
                "name"
            ]
        ],
        "text-max-width": 7
    },
    "paint": {
        "text-opacity": [
            "case",
            [
                "to-boolean",
                [
                    "feature-state",
                    "hide"
                ]
            ],
            0,
            1
        ],
        "icon-opacity": [
            "case",
            [
                "to-boolean",
                [
                    "feature-state",
                    "hide"
                ]
            ],
            0,
            1
        ],
        "text-emissive-strength": [
            "match",
            [
                "config",
                "theme"
            ],
            "monochrome",
            0.6,
            1
        ],
        "icon-emissive-strength": [
            "match",
            [
                "config",
                "theme"
            ],
            "monochrome",
            0.6,
            1
        ],
        "text-color": [
            "case",
            [
                "to-boolean",
                [
                    "feature-state",
                    "select"
                ]
            ],
            [
                "config",
                "colorPlaceLabelSelect"
            ],
            [
                "to-boolean",
                [
                    "feature-state",
                    "highlight"
                ]
            ],
            [
                "config",
                "colorPlaceLabelHighlight"
            ],
            [
                "interpolate",
                [
                    "linear"
                ],
                [
                    "measure-light",
                    "brightness"
                ],
                0.25,
                [
                    "hsl",
                    [
                        "at",
                        0,
                        [
                            "to-hsla",
                            [
                                "config",
                                "colorPlaceLabels"
                            ]
                        ]
                    ],
                    [
                        "at",
                        1,
                        [
                            "to-hsla",
                            [
                                "config",
                                "colorPlaceLabels"
                            ]
                        ]
                    ],
                    80
                ],
                0.3,
                [
                    "config",
                    "colorPlaceLabels"
                ]
            ]
        ],
        "text-halo-color": [
            "interpolate",
            [
                "linear"
            ],
            [
                "measure-light",
                "brightness"
            ],
            0.25,
            "hsla(0, 0%, 20%, 1)",
            0.3,
            [
                "step",
                [
                    "at",
                    2,
                    [
                        "to-hsla",
                        [
                            "config",
                            "colorPlaceLabels"
                        ]
                    ]
                ],
                "hsla(0, 0%, 100%, 1)",
                90,
                "hsla(0, 0%, 60%, 1)"
            ]
        ],
        "text-halo-width": 1,
        "text-halo-blur": 1
    }
}

multiple lines
   {
      "id": "waterl-copy-2",
      "type": "line",
      "source": "openmaptiles",
      "source-layer": "water",
      "paint": {
        "line-color": "rgba(0, 0, 0, 1)",
        "line-blur": 3,
        "line-width": 8
      },
      "layout": {
        "visibility": "visible"
      }
    },
    {
      "id": "waterl-copy",
      "type": "line",
      "source": "openmaptiles",
      "source-layer": "water",
      "paint": {
        "line-color": "rgba(154, 154, 154, 1)",
        "line-width": 4,
        "line-offset": 3
      },
      "layout": {
        "visibility": "visible"
      }
    },
    {
      "id": "waterl",
      "type": "line",
      "source": "openmaptiles",
      "source-layer": "water",
      "paint": {
        "line-color": "rgba(96, 96, 96, 1)",
        "line-offset": 2,
        "line-width": 14,
        "line-blur": 4
      },
      "layout": {
        "visibility": "visible"
      }
    }