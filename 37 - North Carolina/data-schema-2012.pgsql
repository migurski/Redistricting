drop view if exists "nc_votes_2012";
drop table if exists "20121106__nc__general__precinct__raw";

create table "20121106__nc__general__precinct__raw"
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
    "election_day" TEXT,
    "absentee_mail" TEXT,
    "one_stop" TEXT,
    "provisional" TEXT
);

create view "nc_votes_2012" as
with
shapes as (
    select gid AS shape_id, "PREC_ID" as precinct_id, replace("COUNTY_NAM", '_', ' ') as county_name
    from "SBE_PRECINCTS_09012012"
    --where "COUNTY_NAM" = 'BUNCOMBE' and "PREC_ID" = '68.1'
),
votes as (
    select parent_jurisdiction as county_name, jurisdiction as precinct_id,
        (case
         when office = 'PRESIDENT AND VICE PRESIDENT OF THE UNITED STATES' then 'president'
         when office = 'NC GOVERNOR' then 'governor'
         when office = 'US HOUSE OF REPRESENTATIVES' then 'congress'
         else null end) as office,
        district,
        (case
         when party = 'REP' then 'red'
         when party = 'DEM' then 'blue'
         else null end) as party,
        sum(votes::int) as votes
    from "20121106__nc__general__precinct__raw"
    group by parent_jurisdiction, jurisdiction, office, district, party
)
select distinct s.shape_id, s.county_name, s.precinct_id,
    -- President and Governor have no district
    max(pres_red.votes) as pres_red, max(pres_blu.votes) as pres_blue,
    max(gov_red.votes) as gov_red, max(gov_blu.votes) as gov_blue,
    -- Use string_agg on Congressional and State Leg. districts,
    -- because one precinct sometimes votes for different districts.
    string_agg(distinct con_any.district, ',' ORDER BY con_any.district) as con_any_districts,
    max(con_red.votes) as con_red_votes, max(con_blu.votes) as con_blue_votes
from shapes as s
left join votes as v
  on v.county_name = s.county_name and v.precinct_id = s.precinct_id
left join votes as pres_red
  on pres_red.county_name = v.county_name and pres_red.precinct_id = v.precinct_id and pres_red.office = 'president' and pres_red.party = 'red'
left join votes as pres_blu
  on pres_blu.county_name = v.county_name and pres_blu.precinct_id = v.precinct_id and pres_blu.office = 'president' and pres_blu.party = 'blue'
left join votes as gov_red
  on gov_red.county_name = v.county_name and gov_red.precinct_id = v.precinct_id and gov_red.office = 'governor' and gov_red.party = 'red'
left join votes as gov_blu
  on gov_blu.county_name = v.county_name and gov_blu.precinct_id = v.precinct_id and gov_blu.office = 'governor' and gov_blu.party = 'blue'
left join votes as con_any
  on con_any.county_name = v.county_name and con_any.precinct_id = v.precinct_id and con_any.office = 'congress'
left join votes as con_red
  on con_red.county_name = v.county_name and con_red.precinct_id = v.precinct_id and con_red.office = 'congress' and con_red.party = 'red'
left join votes as con_blu
  on con_blu.county_name = v.county_name and con_blu.precinct_id = v.precinct_id and con_blu.office = 'congress' and con_blu.party = 'blue'
group by s.shape_id, s.county_name, s.precinct_id
order by s.county_name, s.precinct_id
;
