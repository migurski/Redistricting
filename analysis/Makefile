CA_Congress.geojson: CA_Congress.csv
	./dissolve.py CA_Congress.csv > CA_Congress.geojson

CA_Assembly.geojson: CA_Assembly.csv
	./dissolve.py CA_Assembly.csv > CA_Assembly.geojson

CA_Senate.geojson: CA_Senate.csv
	./dissolve.py CA_Senate.csv > CA_Senate.geojson

CA_Congress.csv:
	curl -L http://bdistricting.com/2010/CA_Congress/solution.zip -o CA_Congress-solution.zip
	unzip CA_Congress-solution.zip CA_Congress.csv

CA_Assembly.csv:
	curl -L http://bdistricting.com/2010/CA_Assembly/solution.zip -o CA_Assembly-solution.zip
	unzip CA_Assembly-solution.zip CA_Assembly.csv

CA_Senate.csv:
	curl -L http://bdistricting.com/2010/CA_Senate/solution.zip -o CA_Senate-solution.zip
	unzip CA_Senate-solution.zip CA_Senate.csv

tl_2016_06_tabblock10.shp:
	curl -OL https://www2.census.gov/geo/tiger/TIGER2016/TABBLOCK/tl_2016_06_tabblock10.zip
	unzip tl_2016_06_tabblock10.zip

ca-2016: ca-2016/shapefiles/001-alameda.shp ca-2016/shapefiles/001-alameda.dbf ca-2016/shapefiles/001-alameda.prj ca-2016/shapefiles/001-alameda.shx \
         ca-2016/shapefiles/003-alpine.shp ca-2016/shapefiles/003-alpine.dbf ca-2016/shapefiles/003-alpine.prj ca-2016/shapefiles/003-alpine.shx \
         ca-2016/shapefiles/005-amador.shp ca-2016/shapefiles/005-amador.dbf ca-2016/shapefiles/005-amador.prj ca-2016/shapefiles/005-amador.shx \
         ca-2016/shapefiles/007-butte.shp ca-2016/shapefiles/007-butte.dbf ca-2016/shapefiles/007-butte.prj ca-2016/shapefiles/007-butte.shx \
         ca-2016/shapefiles/009-calaveras.shp ca-2016/shapefiles/009-calaveras.dbf ca-2016/shapefiles/009-calaveras.prj ca-2016/shapefiles/009-calaveras.shx \
         ca-2016/shapefiles/011-colusa.shp ca-2016/shapefiles/011-colusa.dbf ca-2016/shapefiles/011-colusa.prj ca-2016/shapefiles/011-colusa.shx \
         ca-2016/shapefiles/013-contra-costa.shp ca-2016/shapefiles/013-contra-costa.dbf ca-2016/shapefiles/013-contra-costa.prj ca-2016/shapefiles/013-contra-costa.shx \
         ca-2016/shapefiles/015-del-norte.shp ca-2016/shapefiles/015-del-norte.dbf ca-2016/shapefiles/015-del-norte.prj ca-2016/shapefiles/015-del-norte.shx \
         ca-2016/shapefiles/017-el-dorado.shp ca-2016/shapefiles/017-el-dorado.dbf ca-2016/shapefiles/017-el-dorado.prj ca-2016/shapefiles/017-el-dorado.shx \
         ca-2016/shapefiles/019-fresno.shp ca-2016/shapefiles/019-fresno.dbf ca-2016/shapefiles/019-fresno.prj ca-2016/shapefiles/019-fresno.shx \
         ca-2016/shapefiles/021-glenn.shp ca-2016/shapefiles/021-glenn.dbf ca-2016/shapefiles/021-glenn.prj ca-2016/shapefiles/021-glenn.shx \
         ca-2016/shapefiles/023-humboldt.shp ca-2016/shapefiles/023-humboldt.dbf ca-2016/shapefiles/023-humboldt.prj ca-2016/shapefiles/023-humboldt.shx \
         ca-2016/shapefiles/025-imperial.shp ca-2016/shapefiles/025-imperial.dbf ca-2016/shapefiles/025-imperial.prj ca-2016/shapefiles/025-imperial.shx \
         ca-2016/shapefiles/027-inyo.shp ca-2016/shapefiles/027-inyo.dbf ca-2016/shapefiles/027-inyo.prj ca-2016/shapefiles/027-inyo.shx \
         ca-2016/shapefiles/029-kern.shp ca-2016/shapefiles/029-kern.dbf ca-2016/shapefiles/029-kern.prj ca-2016/shapefiles/029-kern.shx \
         ca-2016/shapefiles/031-kings.shp ca-2016/shapefiles/031-kings.dbf ca-2016/shapefiles/031-kings.prj ca-2016/shapefiles/031-kings.shx \
         ca-2016/shapefiles/033-lake.shp ca-2016/shapefiles/033-lake.dbf ca-2016/shapefiles/033-lake.prj ca-2016/shapefiles/033-lake.shx \
         ca-2016/shapefiles/035-lassen.shp ca-2016/shapefiles/035-lassen.dbf ca-2016/shapefiles/035-lassen.prj ca-2016/shapefiles/035-lassen.shx \
         ca-2016/shapefiles/037-los-angeles.shp ca-2016/shapefiles/037-los-angeles.dbf ca-2016/shapefiles/037-los-angeles.prj ca-2016/shapefiles/037-los-angeles.shx \
         ca-2016/shapefiles/039-madera.shp ca-2016/shapefiles/039-madera.dbf ca-2016/shapefiles/039-madera.prj ca-2016/shapefiles/039-madera.shx \
         ca-2016/shapefiles/041-marin.shp ca-2016/shapefiles/041-marin.dbf ca-2016/shapefiles/041-marin.prj ca-2016/shapefiles/041-marin.shx \
         ca-2016/shapefiles/043-mariposa.shp ca-2016/shapefiles/043-mariposa.dbf ca-2016/shapefiles/043-mariposa.prj ca-2016/shapefiles/043-mariposa.shx \
         ca-2016/shapefiles/045-mendocino.shp ca-2016/shapefiles/045-mendocino.dbf ca-2016/shapefiles/045-mendocino.prj ca-2016/shapefiles/045-mendocino.shx \
         ca-2016/shapefiles/047-merced.shp ca-2016/shapefiles/047-merced.dbf ca-2016/shapefiles/047-merced.prj ca-2016/shapefiles/047-merced.shx \
         ca-2016/shapefiles/049-modoc.shp ca-2016/shapefiles/049-modoc.dbf ca-2016/shapefiles/049-modoc.prj ca-2016/shapefiles/049-modoc.shx \
         ca-2016/shapefiles/051-mono.shp ca-2016/shapefiles/051-mono.dbf ca-2016/shapefiles/051-mono.prj ca-2016/shapefiles/051-mono.shx \
         ca-2016/shapefiles/053-monterey.shp ca-2016/shapefiles/053-monterey.dbf ca-2016/shapefiles/053-monterey.prj ca-2016/shapefiles/053-monterey.shx \
         ca-2016/shapefiles/055-napa.shp ca-2016/shapefiles/055-napa.dbf ca-2016/shapefiles/055-napa.prj ca-2016/shapefiles/055-napa.shx \
         ca-2016/shapefiles/057-nevada.shp ca-2016/shapefiles/057-nevada.dbf ca-2016/shapefiles/057-nevada.prj ca-2016/shapefiles/057-nevada.shx \
         ca-2016/shapefiles/059-orange.shp ca-2016/shapefiles/059-orange.dbf ca-2016/shapefiles/059-orange.prj ca-2016/shapefiles/059-orange.shx \
         ca-2016/shapefiles/061-placer.shp ca-2016/shapefiles/061-placer.dbf ca-2016/shapefiles/061-placer.prj ca-2016/shapefiles/061-placer.shx \
         ca-2016/shapefiles/063-plumas.shp ca-2016/shapefiles/063-plumas.dbf ca-2016/shapefiles/063-plumas.prj ca-2016/shapefiles/063-plumas.shx \
         ca-2016/shapefiles/065-riverside.shp ca-2016/shapefiles/065-riverside.dbf ca-2016/shapefiles/065-riverside.prj ca-2016/shapefiles/065-riverside.shx \
         ca-2016/shapefiles/067-sacramento.shp ca-2016/shapefiles/067-sacramento.dbf ca-2016/shapefiles/067-sacramento.prj ca-2016/shapefiles/067-sacramento.shx \
         ca-2016/shapefiles/069-san-benito.shp ca-2016/shapefiles/069-san-benito.dbf ca-2016/shapefiles/069-san-benito.prj ca-2016/shapefiles/069-san-benito.shx \
         ca-2016/shapefiles/071-san-bernardino.shp ca-2016/shapefiles/071-san-bernardino.dbf ca-2016/shapefiles/071-san-bernardino.prj ca-2016/shapefiles/071-san-bernardino.shx \
         ca-2016/shapefiles/073-san-diego.shp ca-2016/shapefiles/073-san-diego.dbf ca-2016/shapefiles/073-san-diego.prj ca-2016/shapefiles/073-san-diego.shx \
         ca-2016/shapefiles/075-san-francisco.shp ca-2016/shapefiles/075-san-francisco.dbf ca-2016/shapefiles/075-san-francisco.prj ca-2016/shapefiles/075-san-francisco.shx \
         ca-2016/shapefiles/077-san-joaquin.shp ca-2016/shapefiles/077-san-joaquin.dbf ca-2016/shapefiles/077-san-joaquin.prj ca-2016/shapefiles/077-san-joaquin.shx \
         ca-2016/shapefiles/079-san-luis-obispo.shp ca-2016/shapefiles/079-san-luis-obispo.dbf ca-2016/shapefiles/079-san-luis-obispo.prj ca-2016/shapefiles/079-san-luis-obispo.shx \
         ca-2016/shapefiles/081-san-mateo.shp ca-2016/shapefiles/081-san-mateo.dbf ca-2016/shapefiles/081-san-mateo.prj ca-2016/shapefiles/081-san-mateo.shx \
         ca-2016/shapefiles/083-santa-barbara.shp ca-2016/shapefiles/083-santa-barbara.dbf ca-2016/shapefiles/083-santa-barbara.prj ca-2016/shapefiles/083-santa-barbara.shx \
         ca-2016/shapefiles/085-santa-clara.shp ca-2016/shapefiles/085-santa-clara.dbf ca-2016/shapefiles/085-santa-clara.prj ca-2016/shapefiles/085-santa-clara.shx \
         ca-2016/shapefiles/087-santa-cruz.shp ca-2016/shapefiles/087-santa-cruz.dbf ca-2016/shapefiles/087-santa-cruz.prj ca-2016/shapefiles/087-santa-cruz.shx \
         ca-2016/shapefiles/089-shasta.shp ca-2016/shapefiles/089-shasta.dbf ca-2016/shapefiles/089-shasta.prj ca-2016/shapefiles/089-shasta.shx \
         ca-2016/shapefiles/091-sierra.shp ca-2016/shapefiles/091-sierra.dbf ca-2016/shapefiles/091-sierra.prj ca-2016/shapefiles/091-sierra.shx \
         ca-2016/shapefiles/093-siskiyou.shp ca-2016/shapefiles/093-siskiyou.dbf ca-2016/shapefiles/093-siskiyou.prj ca-2016/shapefiles/093-siskiyou.shx \
         ca-2016/shapefiles/095-solano.shp ca-2016/shapefiles/095-solano.dbf ca-2016/shapefiles/095-solano.prj ca-2016/shapefiles/095-solano.shx \
         ca-2016/shapefiles/097-sonoma.shp ca-2016/shapefiles/097-sonoma.dbf ca-2016/shapefiles/097-sonoma.prj ca-2016/shapefiles/097-sonoma.shx \
         ca-2016/shapefiles/099-stanislaus.shp ca-2016/shapefiles/099-stanislaus.dbf ca-2016/shapefiles/099-stanislaus.prj ca-2016/shapefiles/099-stanislaus.shx \
         ca-2016/shapefiles/101-sutter.shp ca-2016/shapefiles/101-sutter.dbf ca-2016/shapefiles/101-sutter.prj ca-2016/shapefiles/101-sutter.shx \
         ca-2016/shapefiles/103-tehama.shp ca-2016/shapefiles/103-tehama.dbf ca-2016/shapefiles/103-tehama.prj ca-2016/shapefiles/103-tehama.shx \
         ca-2016/shapefiles/105-trinity.shp ca-2016/shapefiles/105-trinity.dbf ca-2016/shapefiles/105-trinity.prj ca-2016/shapefiles/105-trinity.shx \
         ca-2016/shapefiles/107-tulare.shp ca-2016/shapefiles/107-tulare.dbf ca-2016/shapefiles/107-tulare.prj ca-2016/shapefiles/107-tulare.shx \
         ca-2016/shapefiles/109-tuolomne.shp ca-2016/shapefiles/109-tuolomne.dbf ca-2016/shapefiles/109-tuolomne.prj ca-2016/shapefiles/109-tuolomne.shx \
         ca-2016/shapefiles/111-ventura.shp ca-2016/shapefiles/111-ventura.dbf ca-2016/shapefiles/111-ventura.prj ca-2016/shapefiles/111-ventura.shx \
         ca-2016/shapefiles/113-yolo.shp ca-2016/shapefiles/113-yolo.dbf ca-2016/shapefiles/113-yolo.prj ca-2016/shapefiles/113-yolo.shx \
         ca-2016/shapefiles/115-yuba.shp ca-2016/shapefiles/115-yuba.dbf ca-2016/shapefiles/115-yuba.prj ca-2016/shapefiles/115-yuba.shx \
         ca-2016/all_precinct_results.csv

ca-2016/all_precinct_results.csv:
	curl -L https://github.com/datadesk/california-2016-election-precinct-maps/raw/master/final-results/all_precinct_results.csv -o $@

# https://www.gnu.org/software/make/manual/html_node/Pattern-Examples.html
ca-2016/shapefiles/%:
	mkdir -p ca-2016/shapefiles
	curl -L https://github.com/datadesk/california-2016-election-precinct-maps/raw/master/shapefiles/$* -o $@
