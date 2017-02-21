Data
====

Input data comes from U.S. Census shapefiles joined into three national files:
2016 U.S. Congressional districts, State upper house legislative districts, and
State lower house legislative districts.

See `Makefile` for rules on generating input data.

Process
-------

Data is processed in two steps.

1.  `smoosh.py` is used to intersect all combinations of the three types of
    district, resulting in a new Polygon shapefile with GEOID columns
    `uscd_goid` for U.S. Congress, `sldu_geoid` for State legislative district
    upper house, and `sldl_geoid` for State legislative district lower house.
    One additional column `color_id` is generated in QGIS with the [Map Coloring
    plug-in](https://gitlab.com/Balaitous/mapcoloring) to assign different
    colors to neighboring polygons for rendering.
2.  `border.py` is used to generate linear borders between pairs of neighboring
    district combinations, resulting in a new Linestring shapefile with GEOID
    columns `uscdgeoid1`, `sldugeoid1`, and `sldlgeoid1` for districts on one
    side of the border, `uscdgeoid2`, `sldugeoid2`, and `sldlgeoid2` for
    districts on the other, and `uscdborder`, `slduborder`, and `sldlborder`
    flags for whether a line forms one of the three kinds of border.

Output
------

Data is saved to shapefiles and to GeoJSON tiles using `tilestache.cfg`:

- District polygons: [`s3://district-tiles/1/smooshed.zip`](https://s3.amazonaws.com/district-tiles/1/smooshed.zip)
- Linear district boundaries: [`s3://district-tiles/1/bordered.zip`](https://s3.amazonaws.com/district-tiles/1/bordered.zip)
- Sample GeoJSON polygon tile: [`s3://district-tiles/1/smooshed/12/656/1582.geojson.gz`](https://s3.amazonaws.com/district-tiles/1/smooshed/12/656/1582.geojson.gz)
- Sample GeoJSON boundary tile: [`s3://district-tiles/1/bordered/12/656/1582.geojson.gz`](https://s3.amazonaws.com/district-tiles/1/bordered/12/656/1582.geojson.gz)
