nc_votes-2014.csv: SBE_PRECINCTS_20141016.zip 20141104__nc__general__precinct__raw.csv.gz
	./import-data.sh redistrict_nc

SBE_PRECINCTS_20141016.zip:
	curl -L https://github.com/nvkelso/election-geodata/raw/master/data/37-north-carolina/statewide/2014/SBE_PRECINCTS_20141016.zip -o SBE_PRECINCTS_20141016.zip

20141104__nc__general__precinct__raw.csv.gz:
	curl --compress -L https://github.com/openelections/openelections-results-nc/raw/master/raw/20141104__nc__general__precinct__raw.csv -s | gzip --stdout -v9 > 20141104__nc__general__precinct__raw.csv.gz
