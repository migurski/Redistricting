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
