#!/bin/bash -e
DBNAME=$1

unzip -o tl_2016_37_tract.zip

psql $DBNAME -c 'drop view if exists tract_demographics'
shp2pgsql -dID -k -s EPSG:4269 tl_2016_37_tract.shp tl_2016_37_tract | psql $DBNAME

unzip -o 04000US37-B01002.zip
unzip -o 04000US37-B02001.zip
unzip -o 04000US37-B03002.zip
unzip -o 04000US37-B15003.zip
unzip -o 04000US37-B19013.zip

psql $DBNAME < data-schema-census.pgsql
psql $DBNAME <<CONTENT

\copy "acs2015_5yr_B01002" from 'acs2015_5yr_B01002_14000US37001020300/acs2015_5yr_B01002_14000US37001020300.csv' with (format 'csv', header true);
\copy "acs2015_5yr_B02001" from 'acs2015_5yr_B02001_14000US37001020300/acs2015_5yr_B02001_14000US37001020300.csv' with (format 'csv', header true);
\copy "acs2015_5yr_B03002" from 'acs2015_5yr_B03002_14000US37001020300/acs2015_5yr_B03002_14000US37001020300.csv' with (format 'csv', header true);
\copy "acs2015_5yr_B15003" from 'acs2015_5yr_B15003_14000US37001020300/acs2015_5yr_B15003_14000US37001020300.csv' with (format 'csv', header true);
\copy "acs2015_5yr_B19013" from 'acs2015_5yr_B19013_14000US37001020300/acs2015_5yr_B19013_14000US37001020300.csv' with (format 'csv', header true);

CONTENT
