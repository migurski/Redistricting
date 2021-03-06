drop view if exists "nc_votes_2014";
drop table if exists "20141104__nc__general__precinct__raw";

create table "20141104__nc__general__precinct__raw"
(
    "updated_at" TEXT,
    "id" TEXT,
    "start_date" TEXT,
    "end_date" TEXT,
    "election_type" TEXT,
    "result_type" TEXT,
    "special" TEXT,
    "office" TEXT,
    "district" TEXT,
    "name_raw" TEXT,
    "last_name" TEXT,
    "first_name" TEXT,
    "suffix" TEXT,
    "middle_name" TEXT,
    "party" TEXT,
    "parent_jurisdiction" TEXT,
    "jurisdiction" TEXT,
    "division" TEXT,
    "votes" TEXT,
    "votes_type" TEXT,
    "total_votes" TEXT,
    "winner" TEXT,
    "write_in" TEXT,
    "year" TEXT,
    "absentee_by_mail" TEXT,
    "election_day" TEXT,
    "one_stop" TEXT,
    "provisional" TEXT
);

create view "nc_votes_2014" as
with
shapes as (
    select gid AS shape_id, "PREC_ID" as precinct_id, replace("COUNTY_NAM", '_', ' ') as county_name
    from "SBE_PRECINCTS_20141016"
    --where "COUNTY_NAM" = 'BUNCOMBE' and "PREC_ID" = '68.1'
),
votes as (
    select parent_jurisdiction as county_name, jurisdiction as precinct_id,
        (case
         when office = 'US SENATE' then 'senate'
         when office = 'US HOUSE OF REPRESENTATIVES' then 'congress'
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
    -- U.S. Senate has no district
    max(sen_red.votes) as sen_red, max(sen_blu.votes) as sen_blue,
    -- Use string_agg on Congressional and State Leg. districts,
    -- because one precinct sometimes votes for different districts.
    string_agg(distinct con_any.district, ',' ORDER BY con_any.district) as con_districts,
    string_agg(distinct con_race.is_contested, ',') as con_contested,
    max(con_red.votes) as con_red_votes, max(con_blu.votes) as con_blue_votes,
    string_agg(distinct sldu_any.district, ',' ORDER BY sldu_any.district) as sldu_districts,
    string_agg(distinct sldu_race.is_contested, ',') as sldu_contested,
    max(sldu_red.votes) as sldu_red_votes, max(sldu_blu.votes) as sldu_blue_votes,
    string_agg(distinct sldl_any.district, ',' ORDER BY sldl_any.district) as sldl_districts,
    string_agg(distinct sldl_race.is_contested, ',') as sldl_contested,
    max(sldl_red.votes) as sldl_red_votes, max(sldl_blu.votes) as sldl_blue_votes
from shapes as s
left join votes as v
  on v.county_name = s.county_name and v.precinct_id = s.precinct_id
left join votes as sen_red
  on sen_red.county_name = v.county_name and sen_red.precinct_id = v.precinct_id and sen_red.office = 'senate' and sen_red.party = 'red'
left join votes as sen_blu
  on sen_blu.county_name = v.county_name and sen_blu.precinct_id = v.precinct_id and sen_blu.office = 'senate' and sen_blu.party = 'blue'
left join votes as con_any
  on con_any.county_name = v.county_name and con_any.precinct_id = v.precinct_id and con_any.office = 'congress'
left join votes as con_red
  on con_red.county_name = v.county_name and con_red.precinct_id = v.precinct_id and con_red.office = 'congress' and con_red.party = 'red'
left join votes as con_blu
  on con_blu.county_name = v.county_name and con_blu.precinct_id = v.precinct_id and con_blu.office = 'congress' and con_blu.party = 'blue'
left join races as con_race
  on con_race.year = '2014' and con_race.chamber = 'ushouse' and con_race.district_id = con_any.district
left join votes as sldu_any
  on sldu_any.county_name = v.county_name and sldu_any.precinct_id = v.precinct_id and sldu_any.office = 'sldu'
left join votes as sldu_red
  on sldu_red.county_name = v.county_name and sldu_red.precinct_id = v.precinct_id and sldu_red.office = 'sldu' and sldu_red.party = 'red'
left join votes as sldu_blu
  on sldu_blu.county_name = v.county_name and sldu_blu.precinct_id = v.precinct_id and sldu_blu.office = 'sldu' and sldu_blu.party = 'blue'
left join races as sldu_race
  on sldu_race.year = '2014' and sldu_race.chamber = 'sldu' and sldu_race.district_id = sldu_any.district
left join votes as sldl_any
  on sldl_any.county_name = v.county_name and sldl_any.precinct_id = v.precinct_id and sldl_any.office = 'sldl'
left join votes as sldl_red
  on sldl_red.county_name = v.county_name and sldl_red.precinct_id = v.precinct_id and sldl_red.office = 'sldl' and sldl_red.party = 'red'
left join votes as sldl_blu
  on sldl_blu.county_name = v.county_name and sldl_blu.precinct_id = v.precinct_id and sldl_blu.office = 'sldl' and sldl_blu.party = 'blue'
left join races as sldl_race
  on sldl_race.year = '2014' and sldl_race.chamber = 'sldl' and sldl_race.district_id = sldl_any.district
group by s.shape_id, v.county_name, v.precinct_id
order by v.county_name, v.precinct_id
;
