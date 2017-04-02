drop view if exists tract_demographics;
drop table if exists "acs2015_5yr_B01002";
drop table if exists "acs2015_5yr_B02001";
drop table if exists "acs2015_5yr_B03002";
drop table if exists "acs2015_5yr_B15003";
drop table if exists "acs2015_5yr_B19013";

create table "acs2015_5yr_B01002"
(
    "geoid" TEXT,
    "name" TEXT,
    "B01002000.5" FLOAT,
    "B01002000.5, Error" FLOAT,
    "B01002001" FLOAT,          -- overall population median age in years
    "B01002001, Error" FLOAT,
    "B01002002" FLOAT,          -- male population median age in years
    "B01002002, Error" FLOAT,
    "B01002003" FLOAT,          -- female population median age in years
    "B01002003, Error" FLOAT
);

create table "acs2015_5yr_B02001"
(
    "geoid" TEXT,
    "name" TEXT,
    "B02001001" FLOAT,          -- total population
    "B02001001, Error" FLOAT,
    "B02001002" FLOAT,          -- white population
    "B02001002, Error" FLOAT,
    "B02001003" FLOAT,          -- black population
    "B02001003, Error" FLOAT,
    "B02001004" FLOAT,          -- american indian population
    "B02001004, Error" FLOAT,
    "B02001005" FLOAT,          -- asian population
    "B02001005, Error" FLOAT,
    "B02001006" FLOAT,          -- pacific islander population
    "B02001006, Error" FLOAT,
    "B02001007" FLOAT,          -- other race population
    "B02001007, Error" FLOAT,
    "B02001008" FLOAT,          -- two or more races
    "B02001008, Error" FLOAT,
    "B02001009" FLOAT,
    "B02001009, Error" FLOAT,
    "B02001010" FLOAT,
    "B02001010, Error" FLOAT
);

create table "acs2015_5yr_B03002"
(
    "geoid" TEXT,
    "name" TEXT,
    "B03002001" FLOAT,          -- total population
    "B03002001, Error" FLOAT,
    "B03002002" FLOAT,          -- non-hispanic population
    "B03002002, Error" FLOAT,
    "B03002003" FLOAT,          -- non-hispanic white population
    "B03002003, Error" FLOAT,
    "B03002004" FLOAT,          -- non-hispanic black population
    "B03002004, Error" FLOAT,
    "B03002005" FLOAT,          -- non-hispanic american indian population
    "B03002005, Error" FLOAT,
    "B03002006" FLOAT,          -- non-hispanic asian population
    "B03002006, Error" FLOAT,
    "B03002007" FLOAT,          -- non-hispanic pacific islander population
    "B03002007, Error" FLOAT,
    "B03002008" FLOAT,          -- non-hispanic other race population
    "B03002008, Error" FLOAT,
    "B03002009" FLOAT,          -- non-hispanic two or more races
    "B03002009, Error" FLOAT,
    "B03002010" FLOAT,
    "B03002010, Error" FLOAT,
    "B03002011" FLOAT,
    "B03002011, Error" FLOAT,
    "B03002012" FLOAT,          -- hispanic population
    "B03002012, Error" FLOAT,
    "B03002013" FLOAT,          -- hispanic white population
    "B03002013, Error" FLOAT,
    "B03002014" FLOAT,          -- hispanic black population
    "B03002014, Error" FLOAT,
    "B03002015" FLOAT,          -- hispanic american indian population
    "B03002015, Error" FLOAT,
    "B03002016" FLOAT,          -- hispanic asian population
    "B03002016, Error" FLOAT,
    "B03002017" FLOAT,          -- hispanic pacific islander population
    "B03002017, Error" FLOAT,
    "B03002018" FLOAT,          -- hispanic other race population
    "B03002018, Error" FLOAT,
    "B03002019" FLOAT,          -- hispanic two or more races
    "B03002019, Error" FLOAT,
    "B03002020" FLOAT,
    "B03002020, Error" FLOAT,
    "B03002021" FLOAT,
    "B03002021, Error" FLOAT
);

create table "acs2015_5yr_B15003"
(
    "geoid" TEXT,
    "name" TEXT,
    "B15003001" FLOAT,          -- total age 25+ population
    "B15003001, Error" FLOAT,
    "B15003002" FLOAT,
    "B15003002, Error" FLOAT,
    "B15003003" FLOAT,
    "B15003003, Error" FLOAT,
    "B15003004" FLOAT,
    "B15003004, Error" FLOAT,
    "B15003005" FLOAT,
    "B15003005, Error" FLOAT,
    "B15003006" FLOAT,
    "B15003006, Error" FLOAT,
    "B15003007" FLOAT,
    "B15003007, Error" FLOAT,
    "B15003008" FLOAT,
    "B15003008, Error" FLOAT,
    "B15003009" FLOAT,
    "B15003009, Error" FLOAT,
    "B15003010" FLOAT,
    "B15003010, Error" FLOAT,
    "B15003011" FLOAT,
    "B15003011, Error" FLOAT,
    "B15003012" FLOAT,
    "B15003012, Error" FLOAT,
    "B15003013" FLOAT,
    "B15003013, Error" FLOAT,
    "B15003014" FLOAT,
    "B15003014, Error" FLOAT,
    "B15003015" FLOAT,
    "B15003015, Error" FLOAT,
    "B15003016" FLOAT,
    "B15003016, Error" FLOAT,
    "B15003017" FLOAT,          -- age 25+ with high school diploma
    "B15003017, Error" FLOAT,
    "B15003018" FLOAT,          -- age 25+ with GED
    "B15003018, Error" FLOAT,
    "B15003019" FLOAT,          -- age 25+ with <1 year college
    "B15003019, Error" FLOAT,
    "B15003020" FLOAT,          -- age 25+ with 1+ year college, no degree
    "B15003020, Error" FLOAT,
    "B15003021" FLOAT,          -- age 25+ with associate's degree
    "B15003021, Error" FLOAT,
    "B15003022" FLOAT,          -- age 25+ with bachelor's degree
    "B15003022, Error" FLOAT,
    "B15003023" FLOAT,          -- age 25+ with master's degree
    "B15003023, Error" FLOAT,
    "B15003024" FLOAT,          -- age 25+ with professional degree
    "B15003024, Error" FLOAT,
    "B15003025" FLOAT,          -- age 25+ with doctorate degree
    "B15003025, Error" FLOAT
);

create table "acs2015_5yr_B19013"
(
    "geoid" TEXT,
    "name" TEXT,
    "B19013001" FLOAT,          -- median household income
    "B19013001, Error" FLOAT
);



create view tract_demographics as
select
    -- use the shortened tract table GEOID, starting with "37"
    T."GEOID" as geoid, R.name,
    
    -- overall population universe
    "B03002001" as population,
    
    -- white population (non-hispanic)
    "B03002003" as white_pop,

    -- black population (non-hispanic)
    "B03002004" as black_pop,

    -- asian population (non-hispanic)
    "B03002006" as asian_pop,

    -- hispanic population of all races
    "B03002012" as hispanic_pop,

    -- remaining population (non-hispanic)
    ("B03002005"+"B03002007"+"B03002008"+"B03002009") as other_pop,
    
    -- median age in years
    "B01002001" as median_age,
    
    -- median income in dollars
    "B19013001" as median_income,
    
    -- education universe
    "B15003001" as education_pop,
    
    -- no diploma
    ("B15003002"+"B15003003"+"B15003004"+"B15003005"+"B15003006"+"B15003007"+"B15003008"+"B15003009"+"B15003010"+"B15003011"+"B15003012"+"B15003013"+"B15003014"+"B15003015"+"B15003016") as school_pop,
    
    -- high school diploma, GED, or <1 year college
    ("B15003017"+"B15003018"+"B15003019") as diploma_pop,
    
    -- some college, associate's or bachelor's degree
    ("B15003020"+"B15003021"+"B15003022") as college_pop,
    
    -- master's, professional, or doctorate degree
    ("B15003023"+"B15003024"+"B15003025") as graduate_pop,
    
    -- density in people per square kilometer
    (case when T."ALAND" > 0 then "B03002001" / (T."ALAND" / 1000000)
     else null end) as density,
    
    -- land area
    T."ALAND" / 1000000 as area_km2,
     
    T.geom
    
from "tl_2016_37_tract" as T,
     "acs2015_5yr_B03002" as R, "acs2015_5yr_B01002" as A,
     "acs2015_5yr_B19013" as I, "acs2015_5yr_B15003" as E
where R.geoid = '14000US'||T."GEOID"
  and A.geoid = R.geoid
  and I.geoid = R.geoid
  and E.geoid = R.geoid
;
