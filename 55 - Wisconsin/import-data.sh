#!/bin/bash -e
DBNAME=$1

shp2pgsql -s 4269 -dIDk tl_2014_55_county/tl_2014_55_county.shp tl_2014_55_county | psql $DBNAME
shp2pgsql -s 4269 -dIDk tl_2014_55_tract/tl_2014_55_tract.shp | psql $DBNAME

unzip -o 04000US55-050-B02001.zip
unzip -o 04000US55-140-B02001.zip

psql $DBNAME < data-schema.pgsql
psql $DBNAME <<CONTENT

create temporary table _temp_A5B ( like acs2015_5yr_B02001 );

\copy _temp_A5B from 'acs2015_5yr_B02001_05000US55033/acs2015_5yr_B02001_05000US55033.csv' with (format 'csv', header true);
\copy _temp_A5B from 'acs2015_5yr_B02001_14000US55101000800/acs2015_5yr_B02001_14000US55101000800.csv' with (format 'csv', header true);

insert into acs2015_5yr_B02001 select distinct * from _temp_A5B;

\copy tl_2014_55_county_votes from 'tl_2014_55_county-votes.csv' with (format 'csv', header true);
\copy tl_2014_55_tract_votes from 'tl_2014_55_tract-votes.csv' with (format 'csv', header true);
CONTENT
