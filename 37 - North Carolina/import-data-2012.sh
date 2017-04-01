#!/bin/bash -e
DBNAME=$1

unzip -o SBE_PRECINCTS_09012012.zip
gunzip -kf 20121106__nc__general__precinct__raw.csv.gz

psql $DBNAME -c 'drop view if exists "nc_votes_2012"'
shp2pgsql -dID -k -s EPSG:2264 SBE_PRECINCTS_09012012.shp SBE_PRECINCTS_09012012 | psql $DBNAME

psql $DBNAME < data-schema-2012.pgsql
psql $DBNAME <<CONTENT
\copy "20121106__nc__general__precinct__raw" from '20121106__nc__general__precinct__raw.csv' with (format 'csv', header true);
\copy (select * from "nc_votes_2012") to 'nc_votes-2012.csv' with (format 'csv', header true);

CONTENT
