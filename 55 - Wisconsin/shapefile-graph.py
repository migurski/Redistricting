#!/usr/bin/env python3
''' Generate a graph from neighboring census tracts.
'''
import sys, networkx, psycopg2

_, postgres_dsn, table_name, graph_path = sys.argv

graph = networkx.Graph()
networkx.readwrite.write_gml(graph, graph_path)

with psycopg2.connect('postgres://localhost/redistrict_wisconsin') as conn:
    with conn.cursor() as db:
        if table_name == 'tl_2014_55_county':
            prefix = '05000US'
        elif table_name == 'tl_2014_55_tract':
            prefix = '14000US'
        else:
            raise ValueError(table_name)
    
        print('Selecting nodes...', file=sys.stderr)
        db.execute('''select g."GEOID", c."B02001001"
                      from {table} as g, acs2015_5yr_b02001 as c
                      where c.geoid = %s||g."GEOID"
                   '''.format(table=table_name), (prefix, ))
        
        for (geoid, population) in db.fetchall():
            graph.add_node(geoid, population=population)

        print('Found', len(graph.nodes()), 'nodes', file=sys.stderr)

        print('Selecting edges...', file=sys.stderr)
        db.execute('''select c1."GEOID", c2."GEOID"
                      from {table} as c1, {table} as c2
                      where c1."GEOID" < c2."GEOID"
                        and ST_Touches(c1.geom, c2.geom)
                        and ST_GeometryType(ST_Intersection(c1.geom, c2.geom)) != 'ST_Point'
                   '''.format(table=table_name))
        
        for (geoid1, geoid2) in db.fetchall():
            graph.add_edge(geoid1, geoid2)

        print('Found', len(graph.edges()), 'edges', file=sys.stderr)

networkx.readwrite.write_gml(graph, graph_path)
