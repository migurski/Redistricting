drop table if exists "precincts_2014_4269";
drop table if exists precinct_demographics;

create temporary table "precincts_2014_4269"
as
select gid, ST_Transform(geom, 4269) as geom
from "SBE_PRECINCTS_20141016"
--where "COUNTY_NAM" = 'HYDE' and "PREC_ID" = 'LL'
;

select P.gid, T.geoid,
    ST_Area(ST_Intersection(P.geom, T.geom)) / ST_Area(T.geom) as portion
from "precincts_2014_4269" as P
left join tract_demographics as T
  on T.geom && P.geom and ST_Intersects(P.geom, T.geom)
limit 10
;

create temporary table precinct_demographics
as
select shape_id,
    round(sum(T.population * portion)) as population,
    round(sum(T.white_pop * portion)) as white_pop,
    round(sum(T.black_pop * portion)) as black_pop,
    round(sum(T.asian_pop * portion)) as asian_pop,
    round(sum(T.hispanic_pop * portion)) as hispanic_pop,
    round(sum(T.other_pop * portion)) as other_pop,
    round(sum(T.median_age * T.population * portion) / sum(T.population * portion)) as median_age, -- spread out among population count
    round(sum(T.median_income * T.population * portion) / sum(T.population * portion)) as median_income, -- spread out among population count
    round(sum(T.education_pop * portion)) as education_pop,
    round(sum(T.school_pop * portion)) as school_pop,
    round(sum(T.diploma_pop * portion)) as diploma_pop,
    round(sum(T.college_pop * portion)) as college_pop,
    round(sum(T.graduate_pop * portion)) as graduate_pop,
    round(sum(T.area_km2 * portion)) as area_km2
from (
    -- find precinct and tract spatial overlaps, with
    -- portions of tract contained within the precincts.
    select P.gid as shape_id, T."GEOID" as tract_geoid,
        ST_Area(ST_Intersection(P.geom, T.geom)) / ST_Area(T.geom) as portion
    from "precincts_2014_4269" as P
    left join tl_2016_37_tract as T
      on T.geom && P.geom and ST_Intersects(P.geom, T.geom)
    ) as portions,
tract_demographics as T
where T.geoid = tract_geoid
group by shape_id
;

select count(*), sum(population), sum(area_km2), avg(median_age) from tract_demographics;
select count(*), sum(population), sum(area_km2), avg(median_age) from precinct_demographics;
