drop table if exists acs2015_5yr_B02001;
drop table if exists tl_2014_55_county_votes;
drop table if exists tl_2014_55_tract_votes;

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

create table tl_2014_55_county_votes
(
    geoid VARCHAR(5) primary key,
    name TEXT,
    
    CONTOT14 real,
    CONDEM14 real,
    CONREP14 real,
    CONIND14 real,
    CONSCAT14 real,
    CONREP214 real,
    CONIND214 real
);

create table tl_2014_55_tract_votes
(
    geoid VARCHAR(11) primary key,
    name TEXT,
    
    CONTOT14 real,
    CONDEM14 real,
    CONREP14 real,
    CONIND14 real,
    CONSCAT14 real,
    CONREP214 real,
    CONIND214 real
);
