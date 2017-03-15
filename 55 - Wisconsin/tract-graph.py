#!/usr/bin/env python3
''' Generate a graph from neighboring census tracts.
'''
import sys, itertools, networkx
from osgeo import ogr

def get_multilinestring(geometry):
    '''
    '''
    if geometry.GetGeometryType() in (ogr.wkbLineString, ogr.wkbMultiLineString):
        return geometry
    elif geometry.GetGeometryType() == ogr.wkbGeometryCollection:
        multiline = ogr.Geometry(ogr.wkbMultiLineString)
        for geom in geometry:
            if geom.GetGeometryType() == ogr.wkbLineString:
                multiline.AddGeometry(geom)
        return multiline
    else:
        return None

ds = ogr.Open('tl_2014_55_tract/tl_2014_55_tract.shp')
tracts = list(ds.GetLayer(0))
graph = networkx.Graph()

networkx.readwrite.write_edgelist(graph, 'tl_2014_55_tract-edges.txt')

for (tract1, tract2) in itertools.combinations(tracts, 2):
    geom1 = tract1.GetGeometryRef()
    geom2 = tract2.GetGeometryRef()

    if not geom1.Touches(geom2):
        continue
    
    intersection = geom1.Intersection(geom2)
    geometry = get_multilinestring(intersection)
    
    if geometry is None:
        continue
    
    graph.add_edge(tracts.index(tract1), tracts.index(tract2))
    
    print(tracts.index(tract1), tract1.GetField('GEOID'),
          tracts.index(tract2), tract2.GetField('GEOID'),
          file=sys.stderr)

networkx.readwrite.write_edgelist(graph, 'tl_2014_55_tract-edges.txt')
