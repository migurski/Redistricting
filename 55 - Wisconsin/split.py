#!/usr/bin/env python3
import doctest, re, json, csv, sys
from osgeo import ogr

def expand(units):
    '''
    >>> sorted(list(expand('Ward 1')))
    ['Ward 1']
    >>> sorted(list(expand('Ward 1, Ward 2')))
    ['Ward 1', 'Ward 2']
    >>> sorted(list(expand('Ward 1, Ward 2, Ward 3')))
    ['Ward 1', 'Ward 2', 'Ward 3']
    >>> sorted(list(expand('Ward 1B, Ward 2A')))
    ['Ward 1B', 'Ward 2A']
    >>> sorted(list(expand('Ward 1, Wards 3-4')))
    ['Ward 1', 'Ward 3', 'Ward 4']
    >>> sorted(list(expand('Ward 1, Ward 3,4')))
    ['Ward 1', 'Ward 3', 'Ward 4']
    >>> sorted(list(expand('Ward 1, Ward 3,4,5')))
    ['Ward 1', 'Ward 3', 'Ward 4', 'Ward 5']
    >>> sorted(list(expand("Wards 1,8, Wards 2-6, Wards 7,9-11, Ward 12")))
    ['Ward 1', 'Ward 10', 'Ward 11', 'Ward 12', 'Ward 2', 'Ward 3', 'Ward 4', 'Ward 5', 'Ward 6', 'Ward 7', 'Ward 8', 'Ward 9']
    >>> sorted(list(expand("Ward 1,4, Ward 2-3,5")))
    ['Ward 1', 'Ward 2', 'Ward 3', 'Ward 4', 'Ward 5']
    >>> sorted(list(expand("Ward 1,8-11")))
    ['Ward 1', 'Ward 10', 'Ward 11', 'Ward 8', 'Ward 9']
    >>> sorted(list(expand("Ward 1-2,5, Ward 3-4,6")))
    ['Ward 1', 'Ward 2', 'Ward 3', 'Ward 4', 'Ward 5', 'Ward 6']
    >>> sorted(list(expand("Ward 1-3, Ward 4-6, Wards 7-8, Ward 9-11")))
    ['Ward 1', 'Ward 10', 'Ward 11', 'Ward 2', 'Ward 3', 'Ward 4', 'Ward 5', 'Ward 6', 'Ward 7', 'Ward 8', 'Ward 9']
    '''
    wards = set()
    
    for number in re.findall(r'\bward (\w+)\b', units, re.I):
        wards.add('Ward {}'.format(number))
    
    for (start, end) in re.findall(r'\bwards? (\d+)-(\d+)\b', units, re.I):
        for number in range(int(start), int(end) + 1):
            wards.add('Ward {}'.format(number))
    
    for match in re.findall(r'\bwards? ((\w+)(,\w+)+)\b', units, re.I):
        for number in match[0].split(','):
            wards.add('Ward {}'.format(number))
    
    for match in re.findall(r'\bwards? ((\d+-\d+|\d+)(,(\d+-\d+|\d+))+)\b', units, re.I):
        for part in match[0].split(','):
            if '-' in part:
                (start, end) = part.split('-')
                for number in range(int(start), int(end) + 1):
                    wards.add('Ward {}'.format(number))
            else:
                wards.add('Ward {}'.format(part))
    
    return wards

def main(polys_shp, points_csv):
    '''
    '''
    poly_ds = ogr.Open(polys_shp)
    shapes = {F.GetField('gid'): F.GetGeometryRef().ExportToJson() for F in poly_ds.GetLayer(0)}
    
    with open(points_csv) as file:
        input = csv.DictReader(file)
        fieldnames = input.fieldnames
        rows = list(input)
    
    geojson = dict(type='FeatureCollection', features=list())
    
    for row in rows:
        gid = row['gid']
        if gid not in shapes:
            continue
        for unit in expand(row['ReportingUnits']):
            props = dict(row, ReportingUnit=unit, shape_gid=gid, accuracy='Voronoi')
            props.pop('gid')
            props.pop('ReportingUnits')
            geom = json.loads(shapes[gid])
            feat = dict(type='Feature', properties=props, geometry=geom)
            geojson['features'].append(feat)
    
    json.dump(geojson, sys.stdout)
    
if __name__ == '__main__':
    doctest.testmod()
    
    _, polys_shp, points_csv = sys.argv
    exit(main(polys_shp, points_csv))