polling_place_locations_2016_nov_general_xlsx_81288_polygons.geojson: polling_place_locations_2016_nov_general_xlsx_81288_points.csv
	./split.py \
		polling_place_locations_2016_nov_general_xlsx_81288_polygons.shp \
		polling_place_locations_2016_nov_general_xlsx_81288_points.csv > $@

polling_place_locations_2016_nov_general_xlsx_81288_points.gpkg: polling_place_locations_2016_nov_general_xlsx_81288_points.csv
	ogr2ogr -f GPKG -t_srs EPSG:2163 -spat -105 30 -75 55 -overwrite \
		$@ polling_place_locations_2016_nov_general_xlsx_81288_points.vrt

polling_place_locations_2016_nov_general_xlsx_81288_points.csv:
	./prepare.py polling_place_locations_2016_nov_general_xlsx_81288.csv > $@

redistrict_wisconsin: tl_2014_55_tract/tl_2014_55_tract.shp 04000US55-140-B02001.zip \
                      tl_2014_55_county/tl_2014_55_county.shp 04000US55-050-B02001.zip
	./import-data.sh $@

tl_2014_55_tract-edges.txt: tl_2014_55_tract/tl_2014_55_tract.shp
	./shapefile-graph.py $< $@

tl_2014_55_tract/tl_2014_55_tract.shp:
	unzip tl_2014_55_tract.zip

tl_2014_55_county-edges.txt: tl_2014_55_county/tl_2014_55_county.shp
	./shapefile-graph.py $< $@

tl_2014_55_county/tl_2014_55_county.shp:
	unzip tl_2014_55_county.zip

04000US55-050-B02001.zip:
	# URL from Census Reporter: https://censusreporter.org/data/table/?table=B02001&geo_ids=04000US55,050|04000US55&primary_geo_id=04000US55
	curl -L 'https://api.censusreporter.org/1.0/data/download/latest?table_ids=B02001&geo_ids=04000US55,050|04000US55&format=csv' -o $@

04000US55-140-B02001.zip:
	# URL from Census Reporter: https://censusreporter.org/data/table/?table=B02001&geo_ids=04000US55,140|04000US55&primary_geo_id=04000US55
	curl -L 'https://api.censusreporter.org/1.0/data/download/latest?table_ids=B02001&geo_ids=04000US55,140|04000US55&format=csv' -o $@

.PHONY: redistrict_wisconsin