import os, tempfile, tarfile, psycopg2, psycopg2.extras, shutil, operator

def iterate_plans(filename):
    '''
    '''
    dirname = tempfile.mkdtemp(prefix='plans-')

    with tarfile.open(filename, 'r:gz') as file:
        for member in sorted(file, key=operator.attrgetter('path')):
            if member.isreg():
                file.extract(member, path=dirname)
                filepath = os.path.join(dirname, member.path)
                with open(filepath) as plan:
                    print(member.path)
                    yield [int(i) for i in plan.read().split()]
                os.remove(filepath)
    
    shutil.rmtree(dirname)

def calc(districts):
    '''
    '''
    election_votes, wasted_red, wasted_blue, red_wins, blue_wins = 0, 0, 0, 0, 0
    
    for district in districts:
        red_votes = [float(v) for (k, v) in district.items() if 'red' in k.lower()][0]
        blue_votes = [float(v) for (k, v) in district.items() if 'blu' in k.lower()][0]
        district_votes = red_votes + blue_votes
        election_votes += district_votes
        win_threshold = district_votes / 2
    
        if red_votes > blue_votes:
            red_wins += 1
            wasted_red += red_votes - win_threshold # surplus
            wasted_blue += blue_votes # loser
        elif blue_votes > red_votes:
            blue_wins += 1
            wasted_blue += blue_votes - win_threshold # surplus
            wasted_red += red_votes # loser
        else:
            raise ValueError('Unlikely 50/50 split')
    
    return (wasted_blue - wasted_red) / election_votes
        
    print(int(blue_wins), 'blue and', int(red_wins), 'red districts')
    print(int(election_votes), 'total votes')
    print(int(wasted_red), 'wasted red votes')
    print(int(wasted_blue), 'wasted blue votes')
    
    if wasted_blue > wasted_red:
        print('+{:.1f}% gap for red team'.format(100 * (wasted_blue - wasted_red) / election_votes))
    else:
        print('+{:.1f}% gap for blue team'.format(100 * (wasted_red - wasted_blue) / election_votes))

with psycopg2.connect('postgres://localhost/redistrict_wisconsin') as conn:
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as db:
    
        db.execute('''
            drop table if exists county_plans;
            create table county_plans (
                id serial primary key,
                districts integer[],
                population_gap real,
                efficiency_gap real
            );
            ''')
    
        for plan in iterate_plans('out-county.tar.gz'):
            db.execute('insert into county_plans (districts) values (%s)', (plan, ))
            db.execute("select currval('county_plans_id_seq')")
            (plan_id, ) = db.fetchone()
            
            db.execute('''
                select 
                       plan.districts[districts.gid] as district,
                       sum(census."B02001001") as population,
                     --sum(ST_Area(county.geom)) as area,
                       sum(votes.CONTOT14) as total_votes,
                       sum(votes.CONREP14) + sum(votes.CONREP214) as red_votes,
                       sum(votes.CONDEM14) as blue_votes
                from (
                    select id, generate_subscripts(districts, 1) as gid
                    from county_plans where id = %s
                ) as districts
                left join county_plans as plan
                    on plan.id = districts.id
                left join tl_2014_55_county as county
                    on county.gid = districts.gid
                left join acs2015_5yr_b02001 as census
                    on census.geoid = '05000US'||county."GEOID"
                left join tl_2014_55_county_votes as votes
                    on votes.geoid = county."GEOID"
                group by district
                ''', (plan_id, ))
            
            districts = db.fetchall()
            populations = [d['population'] for d in districts]
            
            db.execute('''update county_plans set efficiency_gap = %s,
                          population_gap = %s where id = %s''',
                       (calc(districts), max(populations) / min(populations), plan_id))
