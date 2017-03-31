#!/bin/bash -e
DBNAME=$1

unzip -o SBE_PRECINCTS_20141016.zip
gunzip -kf 20141104__nc__general__precinct__raw.csv.gz

shp2pgsql -dID -k -s EPSG:2264 PRECINCTS.shp SBE_PRECINCTS_20141016 | psql $DBNAME

psql $DBNAME < data-schema.pgsql
psql $DBNAME <<CONTENT
\copy "20141104__nc__general__precinct__raw" from '20141104__nc__general__precinct__raw.csv' with (format 'csv', header true);
CONTENT
