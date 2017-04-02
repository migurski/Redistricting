#!/bin/bash -e
DBNAME=$1

csvcut -c year,chamber,district_id,is_contested nc_races.csv > nc_races-cut.csv

psql $DBNAME < data-schema-races.pgsql
psql $DBNAME <<CONTENT
\copy "races" from 'nc_races-cut.csv' with (format 'csv', header true);

CONTENT
