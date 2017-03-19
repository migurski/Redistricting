import psycopg2, psycopg2.extras
from gap import calc, iterate_plans

with psycopg2.connect('postgres://localhost/redistrict_wisconsin') as conn:
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as db:
    
        db.execute('''
            drop table if exists tract_plans;
            create table tract_plans (
                id serial primary key,
                districts integer[],
                population_gap real,
                efficiency_gap real
            );
            ''')
    
        for plan in iterate_plans('out-tracts-10k.tar.gz'):
            db.execute('insert into tract_plans (districts) values (%s)', (plan, ))
            db.execute("select currval('tract_plans_id_seq')")
            (plan_id, ) = db.fetchone()
            
            db.execute('''
                select 
                       plan.districts[districts.gid] as district,
                       sum(census."B02001001") as population,
                     --sum(ST_Area(tract.geom)) as area,
                       sum(votes.CONTOT14) as total_votes,
                       sum(votes.CONREP14) + sum(votes.CONREP214) as red_votes,
                       sum(votes.CONDEM14) as blue_votes
                from (
                    select id, generate_subscripts(districts, 1) as gid
                    from tract_plans where id = %s
                ) as districts
                left join tract_plans as plan
                    on plan.id = districts.id
                left join tl_2014_55_tract as tract
                    on tract.gid = districts.gid
                left join acs2015_5yr_b02001 as census
                    on census.geoid = '14000US'||tract."GEOID"
                left join tl_2014_55_tract_votes as votes
                    on votes.geoid = tract."GEOID"
                group by district
                ''', (plan_id, ))
            
            districts = db.fetchall()
            populations = [d['population'] for d in districts]
            
            db.execute('''update tract_plans set efficiency_gap = %s,
                          population_gap = %s where id = %s''',
                       (calc(districts), max(populations) / min(populations), plan_id))
