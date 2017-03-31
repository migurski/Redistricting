#!/bin/bash -e
DBNAME=$1

unzip -o SBE_PRECINCTS_20141016.zip
gunzip -kf 20141104__nc__general__precinct__raw.csv.gz

shp2pgsql -dID -k -s EPSG:2264 PRECINCTS.shp SBE_PRECINCTS_20141016 | psql $DBNAME

psql $DBNAME < data-schema.pgsql
psql $DBNAME <<CONTENT
\copy "20141104__nc__general__precinct__raw" from '20141104__nc__general__precinct__raw.csv' with (format 'csv', header true);

create temporary table nc_votes as
with
shapes as (
    select gid AS shape_id, "PREC_ID" as precinct_id, replace("COUNTY_NAM", '_', ' ') as county_name
    from "SBE_PRECINCTS_20141016"
    --where "COUNTY_NAM" = 'NEW_HANOVER'
),
votes as (
    select parent_jurisdiction as county_name, jurisdiction as precinct_id,
        (case
         when office = 'US SENATE' then 'senate'
         when office = 'US HOUSE OF REPRESENTATIVES' then 'uscd'
         when office = 'NC STATE SENATE' then 'sldu'
         when office = 'NC HOUSE OF REPRESENTATIVES' then 'sldl'
         else null end) as office,
        district,
        (case
         when party = 'REP' then 'red'
         when party = 'DEM' then 'blue'
         else null end) as party,
        sum(votes::int) as votes
    from "20141104__nc__general__precinct__raw"
    group by parent_jurisdiction, jurisdiction, office, district, party
)
select distinct s.shape_id, v.county_name, v.precinct_id,
    sum(sen_red.votes) as sen_red, sum(sen_blu.votes) as sen_blue,
    string_agg(distinct uscd_red.district, ',' ORDER BY uscd_red.district) as uscd_districts, sum(uscd_red.votes) as uscd_red, sum(uscd_blu.votes) as uscd_blue,
    string_agg(distinct sldu_red.district, ',' ORDER BY sldu_red.district) as sldu_districts, sum(sldu_red.votes) as sldu_red, sum(sldu_blu.votes) as sldu_blue,
    string_agg(distinct sldl_red.district, ',' ORDER BY sldl_red.district) as sldl_districts, sum(sldl_red.votes) as sldl_red, sum(sldl_blu.votes) as sldl_blue
from shapes as s
left join votes as v
  on v.county_name = s.county_name and v.precinct_id = s.precinct_id
left join votes as sen_red
  on sen_red.county_name = v.county_name and sen_red.precinct_id = v.precinct_id and sen_red.office = 'senate' and sen_red.party = 'red'
left join votes as sen_blu
  on sen_blu.county_name = v.county_name and sen_blu.precinct_id = v.precinct_id and sen_blu.office = 'senate' and sen_blu.party = 'blue'
left join votes as uscd_red
  on uscd_red.county_name = v.county_name and uscd_red.precinct_id = v.precinct_id and uscd_red.office = 'uscd' and uscd_red.party = 'red'
left join votes as uscd_blu
  on uscd_blu.county_name = v.county_name and uscd_blu.precinct_id = v.precinct_id and uscd_blu.office = 'uscd' and uscd_blu.party = 'blue'
left join votes as sldu_red
  on sldu_red.county_name = v.county_name and sldu_red.precinct_id = v.precinct_id and sldu_red.office = 'sldu' and sldu_red.party = 'red'
left join votes as sldu_blu
  on sldu_blu.county_name = v.county_name and sldu_blu.precinct_id = v.precinct_id and sldu_blu.office = 'sldu' and sldu_blu.party = 'blue'
left join votes as sldl_red
  on sldl_red.county_name = v.county_name and sldl_red.precinct_id = v.precinct_id and sldl_red.office = 'sldl' and sldl_red.party = 'red'
left join votes as sldl_blu
  on sldl_blu.county_name = v.county_name and sldl_blu.precinct_id = v.precinct_id and sldl_blu.office = 'sldl' and sldl_blu.party = 'blue'
group by s.shape_id, v.county_name, v.precinct_id
order by v.county_name, v.precinct_id
;

\copy "nc_votes" to 'nc_votes-2014.csv' with (format 'csv', header true);

CONTENT
