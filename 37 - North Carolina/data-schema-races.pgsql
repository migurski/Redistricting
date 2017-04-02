drop table if exists races cascade;

create table races
(
    year        TEXT,
    chamber     TEXT,
    district_id TEXT,
    is_contested TEXT
);
