''' Smoosh three different kinds of districts together into a new shapefile.

Intersects three layers of districts to generate a new quilt of district areas.
Outputs shapefile name to stdout.
'''
import itertools, tempfile, os, sys
from osgeo import ogr

# Prepare input data sources.
all_sldu_ds = ogr.Open('tl_2016_all_sldu.shp')
all_sldl_ds = ogr.Open('tl_2016_all_sldl.shp')
us_cd115_ds = ogr.Open('tl_2016_us_cd115.shp')

all_sldu_lyr = list(all_sldu_ds.GetLayer(0))
all_sldl_lyr = list(all_sldl_ds.GetLayer(0))
us_cd115_lyr = list(us_cd115_ds.GetLayer(0))

# Prepare output data source.
out_path = os.path.join(tempfile.mkdtemp(dir='.', prefix='smooshed-'), 'smooshed.shp')
out_ds = ogr.GetDriverByName('ESRI Shapefile').CreateDataSource(out_path, ['ENCODING=UTF8'])
out_lyr = out_ds.CreateLayer('things', us_cd115_ds.GetLayer(0).GetSpatialRef(), ogr.wkbMultiPolygon)
out_lyr.CreateField(ogr.FieldDefn('sldu_geoid', ogr.OFTString))
out_lyr.CreateField(ogr.FieldDefn('sldl_geoid', ogr.OFTString))
out_lyr.CreateField(ogr.FieldDefn('uscd_geoid', ogr.OFTString))

# Iterate over every U.S. state separately by FIPS code.
fips_codes = {feat.GetField('STATEFP') for feat in us_cd115_lyr}

def get_polygon_geometries(geometry):
    '''
    '''
    if geometry.GetGeometryType() == ogr.wkbPolygon:
        return [geometry]
    elif geometry.GetGeometryType() in (ogr.wkbMultiPolygon, ogr.wkbGeometryCollection):
        return [geom for geom in geometry if geom.GetGeometryType() == ogr.wkbPolygon]
    else:
        return []

def add_new_feature(layer, geometry, sldu_geoid, sldl_geoid, uscd_geoid):
    '''
    '''
    print(index, uscd_geoid, sldu_geoid, sldl_geoid, file=sys.stderr)

    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetGeometry(geometry)
    feature.SetField('sldu_geoid', sldu_geoid)
    feature.SetField('sldl_geoid', sldl_geoid)
    feature.SetField('uscd_geoid', uscd_geoid)
    layer.CreateFeature(feature)

for fips_code in sorted(fips_codes):
    # Isolate features for this one U.S. state.
    all_sldu_fs = [feat for feat in all_sldu_lyr if feat.GetField('STATEFP') == fips_code]
    all_sldl_fs = [feat for feat in all_sldl_lyr if feat.GetField('STATEFP') == fips_code]
    us_cd115_fs = [feat for feat in us_cd115_lyr if feat.GetField('STATEFP') == fips_code]
    
    if not all_sldl_fs:
        # Nebraska and D.C. have only an upper house defined:
        # http://www.census.gov/geo/reference/gtc/gtc_sld.html
        all_sldl_fs = [None]
    
    product = itertools.product(all_sldu_fs, all_sldl_fs, us_cd115_fs)
    
    # Iterate over all possible district combinations.
    for (all_sldu_feat, all_sldl_feat, us_cd115_feat) in product:
        if all_sldl_feat is None:
            # Nebraska and D.C. have only an upper house defined.
            all_sldu_geom = all_sldu_feat.GetGeometryRef()
            us_cd115_geom = us_cd115_feat.GetGeometryRef()
        
            # Pass if this pair of geometries does not intersect
            if us_cd115_geom.Disjoint(all_sldu_geom):
                continue
            if us_cd115_geom.Touches(all_sldu_geom):
                continue
        
            # Calculate the intersection, and collect any polygonal areas.
            intersection = all_sldu_geom.Intersection(us_cd115_geom)
            geoms = get_polygon_geometries(intersection)
        
            # Write a new feature for each polygon found.
            for (index, geom) in enumerate(geoms):
                sldu_geoid = all_sldu_feat.GetField('GEOID')
                uscd_geoid = us_cd115_feat.GetField('GEOID')
                add_new_feature(out_lyr, geom, sldu_geoid, '', uscd_geoid)
        else:
            all_sldu_geom = all_sldu_feat.GetGeometryRef()
            all_sldl_geom = all_sldl_feat.GetGeometryRef()
            us_cd115_geom = us_cd115_feat.GetGeometryRef()
        
            # Pass if any pair of geometries does not intersect
            if all_sldu_geom.Disjoint(all_sldl_geom):
                continue
            if all_sldl_geom.Disjoint(us_cd115_geom):
                continue
            if us_cd115_geom.Disjoint(all_sldu_geom):
                continue
            if all_sldu_geom.Touches(all_sldl_geom):
                continue
            if all_sldl_geom.Touches(us_cd115_geom):
                continue
            if us_cd115_geom.Touches(all_sldu_geom):
                continue
        
            # Calculate the intersection, and collect any polygonal areas.
            intersection = all_sldu_geom.Intersection(all_sldl_geom.Intersection(us_cd115_geom))
            geoms = get_polygon_geometries(intersection)
        
            # Write a new feature for each polygon found.
            for (index, geom) in enumerate(geoms):
                sldu_geoid = all_sldu_feat.GetField('GEOID')
                sldl_geoid = all_sldl_feat.GetField('GEOID')
                uscd_geoid = us_cd115_feat.GetField('GEOID')
                add_new_feature(out_lyr, geom, sldu_geoid, sldl_geoid, uscd_geoid)

print(out_path, file=sys.stdout)
out_ds.Destroy()
