#!/usr/bin/env python3
''' Dissolve a bdistricting.com CSV of Census block GEOIDs and district IDs.

Outputs resulting GeoJSON to stdout.
'''
import sys, csv, osgeo.ogr, itertools, json

def dissolve(geoms, depth=1):
    '''
    '''
    if len(geoms) >= 2:
        center = len(geoms) // 2
        geom1 = dissolve(geoms[:center], depth + 1)
        geom2 = dissolve(geoms[center:], depth + 1)

        #print(' ' * depth, len(geoms), file=sys.stderr)
        return geom1.Union(geom2)

    elif len(geoms) == 1:
        return geoms[0]

    raise ValueError('Zero geoms is weird')

def main(bdistrict_path):
    '''
    '''
    with open(bdistrict_path) as file:
        rows = csv.reader(file)
        districts = {precint: int(district) for (precint, district) in rows}
    
    print(len(districts), 'blocks and',
          len(set(districts.values())), 'districts', file=sys.stderr)
    
    sort_func = lambda F: (districts.get(F.GetField('GEOID10')), F.GetField('INTPTLAT10'))
    group_func = lambda F: districts.get(F.GetField('GEOID10'))
    
    print('Loading and sorting...', file=sys.stderr)
    ds = osgeo.ogr.Open('tl_2016_06_tabblock10.shp')
    layer = ds.GetLayer(0)
    in_features = sorted(layer, key=sort_func)
    out_strings = list()
    
    for (district_id, key_features) in itertools.groupby(in_features, key=group_func):
        geoms = [feat.GetGeometryRef() for feat in key_features]
        print(len(geoms), 'geometries in district', district_id, file=sys.stderr)
        
        geom = dissolve(geoms)
        out_feature = dict(type='Feature')
        out_feature.update(properties={'District': district_id})
        out_feature.update(geometry=None)

        # Output strings so we can lean on OGR's nicer JSON export
        out_str = json.dumps(out_feature).replace('null', geom.ExportToJson())
        out_strings.append(out_str)

        # if len(out_strings) == 10:
        #     break
    
    out_geojson = dict(type='FeatureCollection', features=[None])
    out_str = json.dumps(out_geojson).replace('null', ', '.join(out_strings))
    print(out_str, file=sys.stdout)

if __name__ == '__main__':
    _, bdistrict_path = sys.argv
    exit(main(bdistrict_path))
