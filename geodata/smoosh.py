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

for fips_code in sorted(fips_codes):
    # Isolate feature for this one U.S. state.
    all_sldu_fs = [feat for feat in all_sldu_lyr if feat.GetField('STATEFP') == fips_code]
    all_sldl_fs = [feat for feat in all_sldl_lyr if feat.GetField('STATEFP') == fips_code]
    us_cd115_fs = [feat for feat in us_cd115_lyr if feat.GetField('STATEFP') == fips_code]
    
    product = itertools.product(all_sldu_fs, all_sldl_fs, us_cd115_fs)
    
    # Iterate over all possible district combinations.
    for (all_sldu_feat, all_sldl_feat, us_cd115_feat) in product:
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
        
        if intersection.GetGeometryType() == ogr.wkbPolygon:
            geoms = [intersection]
        elif intersection.GetGeometryType() in (ogr.wkbMultiPolygon, ogr.wkbGeometryCollection):
            geoms = [geom for geom in intersection if geom.GetGeometryType() == ogr.wkbPolygon]
        else:
            geoms = []
        
        # Write a new feature for each polygon found.
        for (index, geom) in enumerate(geoms):
            sldu_geoid = all_sldu_feat.GetField('GEOID')
            sldl_geoid = all_sldl_feat.GetField('GEOID')
            uscd_geoid = us_cd115_feat.GetField('GEOID')
        
            print(index, sldu_geoid, sldl_geoid, uscd_geoid, file=sys.stderr)
        
            out_feat = ogr.Feature(out_lyr.GetLayerDefn())
            out_feat.SetGeometry(geom)
            out_feat.SetField('sldu_geoid', sldu_geoid)
            out_feat.SetField('sldl_geoid', sldl_geoid)
            out_feat.SetField('uscd_geoid', uscd_geoid)
            out_lyr.CreateFeature(out_feat)

print(out_path, file=sys.stdout)
out_ds.Destroy()
