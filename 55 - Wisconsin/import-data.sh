#!/bin/bash -e
DBNAME=$1

shp2pgsql -s 4269 -dIDk tl_2014_55_county/tl_2014_55_county.shp tl_2014_55_county | psql $DBNAME
shp2pgsql -s 4269 -dIDk tl_2014_55_tract/tl_2014_55_tract.shp | psql $DBNAME

unzip -o 04000US55-050-B02001.zip
unzip -o 04000US55-140-B02001.zip

psql $DBNAME <<SCHEMA
drop table if exists acs2015_5yr_B02001;

create table acs2015_5yr_B02001
(
    geoid VARCHAR(18) primary key,
    name TEXT,

    -- Total
    "B02001001" integer,
    "B02001001, Error" integer,
    -- White alone
    "B02001002" integer,
    "B02001002, Error" integer,
    -- Black or African American alone
    "B02001003" integer,
    "B02001003, Error" integer,
    -- American Indian and Alaska Native alone
    "B02001004" integer,
    "B02001004, Error" integer,
    -- Asian alone
    "B02001005" integer,
    "B02001005, Error" integer,
    -- Native Hawaiian and Other Pacific Islander alone
    "B02001006" integer,
    "B02001006, Error" integer,
    -- Some other race alone
    "B02001007" integer,
    "B02001007, Error" integer,
    -- Two or more races
    "B02001008" integer,
    "B02001008, Error" integer,
    -- Two races including Some other race
    "B02001009" integer,
    "B02001009, Error" integer,
    -- Two races excluding Some other race, and three or more races
    "B02001010" integer,
    "B02001010, Error" integer
);

create temporary table _temp_A5B ( like acs2015_5yr_B02001 );

\copy _temp_A5B from 'acs2015_5yr_B02001_05000US55033/acs2015_5yr_B02001_05000US55033.csv' with (format 'csv', header true);
\copy _temp_A5B from 'acs2015_5yr_B02001_14000US55101000800/acs2015_5yr_B02001_14000US55101000800.csv' with (format 'csv', header true);

insert into acs2015_5yr_B02001 select distinct * from _temp_A5B;
SCHEMA
