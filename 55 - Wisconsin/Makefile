polling_place_locations_2016_nov_general_xlsx_81288_polygons.geojson: polling_place_locations_2016_nov_general_xlsx_81288_points.csv
	./split.py \
		polling_place_locations_2016_nov_general_xlsx_81288_polygons.shp \
		polling_place_locations_2016_nov_general_xlsx_81288_points.csv > $@

polling_place_locations_2016_nov_general_xlsx_81288_points.gpkg: polling_place_locations_2016_nov_general_xlsx_81288_points.csv
	ogr2ogr -f GPKG -t_srs EPSG:2163 -spat -105 30 -75 55 -overwrite \
		$@ polling_place_locations_2016_nov_general_xlsx_81288_points.vrt

polling_place_locations_2016_nov_general_xlsx_81288_points.csv:
	./prepare.py polling_place_locations_2016_nov_general_xlsx_81288.csv > $@

tl_2014_55_tract-edges.txt: tl_2014_55_tract/tl_2014_55_tract.shp
	./tract-graph.py

tl_2014_55_tract/tl_2014_55_tract.shp:
	unzip tl_2014_55_tract.zip