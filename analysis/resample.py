#!/usr/bin/env python3
''' Distributes numbers from a votes shapefile to a plan shapefile.

The votes come in precincts and represent real-world numbers of human votes.
See rules for `precincts-buffered.shp` from the Makefile for details on this.
A plan is a set of districts that might be real or imaginary. This script
spatially distributes numeric counts from the voting precincts to the planned
districts.
'''
import sys, os, tempfile
from osgeo import ogr

ogr.UseExceptions()

def apply_fields(from_layer, to_layer, types):
    '''
    '''
    names = []
    from_defn = from_layer.GetLayerDefn()
    for index in range(from_defn.GetFieldCount()):
        field = from_defn.GetFieldDefn(index)
        if not types or field.type in types:
            print(field.name, field.type, file=sys.stderr)
            to_layer.CreateField(ogr.FieldDefn(field.name, field.type))
            names.append(field.name)
    return names

def main(votes_path, plan_path):
    '''
    '''
    votes_ds = ogr.Open(votes_path)
    plan_ds = ogr.Open(plan_path)
    
    votes_lyr = votes_ds.GetLayer(0)
    plan_lyr = plan_ds.GetLayer(0)
    
    # if str(votes_lyr.GetSpatialRef()) != str(plan_lyr.GetSpatialRef()):
    #     raise ValueError('Input projections have to match')
    
    out_path = os.path.join(tempfile.mkdtemp(dir='.', prefix='resampled-'), 'resampled.shp')
    out_ds = ogr.GetDriverByName('ESRI Shapefile').CreateDataSource(out_path, ['ENCODING=UTF8'])
    out_lyr = out_ds.CreateLayer('things', plan_lyr.GetSpatialRef(), ogr.wkbMultiPolygon)
    
    plan_names = apply_fields(plan_lyr, out_lyr, None)
    votes_names = apply_fields(votes_lyr, out_lyr, (ogr.OFTInteger, ogr.OFTReal))
    
    # Iterate over plan districts accumulating data from the vote precincts layer.
    
    included_precincts, skipped_precincts = set(), set()
    
    for plan_feature in plan_lyr:
        plan_geom = plan_feature.GetGeometryRef()
        out_feature = ogr.Feature(out_lyr.GetLayerDefn())
        
        # Iterate over precincts that might overlap the current planned district.
    
        votes_lyr.SetSpatialFilter(plan_geom)
        votes_fields = {name: 0 for name in votes_names}
        
        for votes_feature in votes_lyr:
            precinct_id = votes_feature.GetField('pct16')
            votes_geom = votes_feature.GetGeometryRef()
            if not votes_geom:
                should_skip = True
            else:
                try:
                    should_skip = votes_geom.Disjoint(plan_geom)
                except RuntimeError:
                    print('Disjoint oops', precinct_id, votes_geom.IsValid(), file=sys.stderr)
                    should_skip = True
            if should_skip:
                skipped_precincts.add(precinct_id)
                continue
            try:
                intersect_geom = votes_geom.Intersection(plan_geom)
            except RuntimeError:
                print('Intersection oops', precinct_id, votes_geom.IsValid(), file=sys.stderr)
                should_skip = True
            else:
                should_skip = False
            if should_skip:
                skipped_precincts.add(precinct_id)
                continue
            
            included_precincts.add(precinct_id)

            # Apply a fraction of the precinct totals to the district by area.
            
            intersect_fraction = intersect_geom.Area() / votes_geom.Area()
            
            for name in votes_fields:
                votes_fields[name] += intersect_fraction * votes_feature.GetField(name)
        
        # Finish the planned district and move on.
        
        for (name, value) in votes_fields.items():
            out_feature.SetField(name, value)
        
        for name in plan_names:
            out_feature.SetField(name, plan_feature.GetField(name))
        
        out_feature.SetGeometry(plan_feature.GetGeometryRef())
        out_lyr.CreateFeature(out_feature)
        print('.', file=sys.stderr)
    
    # print('Skipped and included:', skipped_precincts & included_precincts, file=sys.stderr)
    # print('Skipped only:', skipped_precincts - included_precincts, file=sys.stderr)
    
    out_ds.Destroy()
    print(out_path, file=sys.stdout)

if __name__ == '__main__':
    _, votes_path, plan_path = sys.argv
    exit(main(votes_path, plan_path))