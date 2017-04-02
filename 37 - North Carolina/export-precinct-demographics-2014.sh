#!/bin/bash -e
DBNAME=$1
FILENAME=$2

psql $DBNAME <<CONTENT
\i precincts-demographics-query.pgsql
\copy "precinct_demographics" to 'nc_demographics-2014.csv' with (format 'csv', header true);

CONTENT

csvjoin -c shape_id nc_votes-2014.csv nc_demographics-2014.csv > $FILENAME
