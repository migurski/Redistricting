nc_complete-2014.csv: nc_votes-2014.csv
	./export-precinct-demographics-2014.sh redistrict_nc $@

nc_votes-2014.csv: SBE_PRECINCTS_20141016.zip 20141104__nc__general__precinct__raw.csv.gz
	./import-data-2014.sh redistrict_nc

nc_votes-2012.csv: SBE_PRECINCTS_09012012.zip 20121106__nc__general__precinct__raw.csv.gz
	./import-data-2012.sh redistrict_nc

SBE_PRECINCTS_20141016.zip:
	curl -L https://github.com/nvkelso/election-geodata/raw/master/data/37-north-carolina/statewide/2014/SBE_PRECINCTS_20141016.zip -o SBE_PRECINCTS_20141016.zip

20141104__nc__general__precinct__raw.csv.gz:
	curl --compress -L https://github.com/openelections/openelections-results-nc/raw/master/raw/20141104__nc__general__precinct__raw.csv -s | gzip --stdout -v9 > 20141104__nc__general__precinct__raw.csv.gz

SBE_PRECINCTS_09012012.zip:
	curl -L https://github.com/nvkelso/election-geodata/raw/master/data/37-north-carolina/statewide/2012/SBE_PRECINCTS_09012012.zip -o SBE_PRECINCTS_09012012.zip

20121106__nc__general__precinct__raw.csv.gz:
	curl --compress -L https://github.com/openelections/openelections-results-nc/raw/master/raw/20121106__nc__general__precinct__raw.csv -s | gzip --stdout -v9 > 20121106__nc__general__precinct__raw.csv.gz

census: tl_2016_37_tract.zip 04000US37-B01002.zip 04000US37-B02001.zip \
        04000US37-B03002.zip 04000US37-B15003.zip 04000US37-B19013.zip
	./import-census.sh redistrict_nc

tl_2016_37_tract.zip:
	# Census tracts
	curl -L 'https://www2.census.gov/geo/tiger/TIGER2016/TRACT/tl_2016_37_tract.zip' -o $@

04000US37-B01002.zip:
	# Median age
	# URL from Census Reporter: https://censusreporter.org/data/table/?geo_ids=04000US37,140|04000US37&primary_geo_id=04000US37&table=B01002
	curl -L 'https://api.censusreporter.org/1.0/data/download/latest?geo_ids=04000US37,140|04000US37&format=csv&table_ids=B01002' -o $@

04000US37-B02001.zip:
	# Race
	# URL from Census Reporter: https://censusreporter.org/data/table/?geo_ids=04000US37,140|04000US37&primary_geo_id=04000US37&table=B02001
	curl -L 'https://api.censusreporter.org/1.0/data/download/latest?geo_ids=04000US37,140|04000US37&format=csv&table_ids=B02001' -o $@

04000US37-B03002.zip:
	# Race + hispanic
	# URL from Census Reporter: https://censusreporter.org/data/table/?geo_ids=04000US37,140|04000US37&primary_geo_id=04000US37&table=B03002
	curl -L 'https://api.censusreporter.org/1.0/data/download/latest?geo_ids=04000US37,140|04000US37&format=csv&table_ids=B03002' -o $@

04000US37-B15003.zip:
	# Educational attainment
	# URL from Census Reporter: https://censusreporter.org/data/table/?geo_ids=04000US37,140|04000US37&primary_geo_id=04000US37&table=B15003
	curl -L 'https://api.censusreporter.org/1.0/data/download/latest?geo_ids=04000US37,140|04000US37&format=csv&table_ids=B15003' -o $@

04000US37-B19013.zip:
	# Median income
	# URL from Census Reporter: https://censusreporter.org/data/table/?geo_ids=04000US37,140|04000US37&primary_geo_id=04000US37&table=B19013
	curl -L 'https://api.censusreporter.org/1.0/data/download/latest?geo_ids=04000US37,140|04000US37&format=csv&table_ids=B19013' -o $@

.PHONY: census
