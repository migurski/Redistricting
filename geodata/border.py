import itertools, tempfile, sys, os
from osgeo import ogr

input_ds = ogr.Open('smooshed.shp')
input_lyr = list(input_ds.GetLayer(0))

# Prepare output data source.
out_path = os.path.join(tempfile.mkdtemp(dir='.', prefix='bordered-'), 'bordered.shp')
out_ds = ogr.GetDriverByName('ESRI Shapefile').CreateDataSource(out_path, ['ENCODING=UTF8'])
out_lyr = out_ds.CreateLayer('things', input_ds.GetLayer(0).GetSpatialRef(), ogr.wkbMultiLineString)
out_lyr.CreateField(ogr.FieldDefn('sldugeoid1', ogr.OFTString))
out_lyr.CreateField(ogr.FieldDefn('sldlgeoid1', ogr.OFTString))
out_lyr.CreateField(ogr.FieldDefn('uscdgeoid1', ogr.OFTString))
out_lyr.CreateField(ogr.FieldDefn('sldugeoid2', ogr.OFTString))
out_lyr.CreateField(ogr.FieldDefn('sldlgeoid2', ogr.OFTString))
out_lyr.CreateField(ogr.FieldDefn('uscdgeoid2', ogr.OFTString))
out_lyr.CreateField(ogr.FieldDefn('slduborder', ogr.OFTInteger))
out_lyr.CreateField(ogr.FieldDefn('sldlborder', ogr.OFTInteger))
out_lyr.CreateField(ogr.FieldDefn('uscdborder', ogr.OFTInteger))

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

def add_new_feature(layer, geometry, sldugeoid1, sldlgeoid1, uscdgeoid1, sldugeoid2, sldlgeoid2, uscdgeoid2):
    '''
    '''
    print(sldugeoid1, sldlgeoid1, uscdgeoid1, sldugeoid2, sldlgeoid2, uscdgeoid2, file=sys.stderr)

    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetGeometry(geometry)
    feature.SetField('sldugeoid1', sldugeoid1)
    feature.SetField('sldlgeoid1', sldlgeoid1)
    feature.SetField('uscdgeoid1', uscdgeoid1)
    feature.SetField('sldugeoid2', sldugeoid2)
    feature.SetField('sldlgeoid2', sldlgeoid2)
    feature.SetField('uscdgeoid2', uscdgeoid2)
    feature.SetField('slduborder', int(sldugeoid1 != sldugeoid2))
    feature.SetField('sldlborder', int(sldlgeoid1 != sldlgeoid2))
    feature.SetField('uscdborder', int(uscdgeoid1 != uscdgeoid2))
    layer.CreateFeature(feature)

count = 0

for (feature1, feature2) in itertools.combinations(input_lyr, 2):
    geom1 = feature1.GetGeometryRef()
    geom2 = feature2.GetGeometryRef()

    if not geom1.Touches(geom2):
        continue

    intersection = geom1.Intersection(geom2)
    geometry = get_multilinestring(intersection)
    
    if geometry is None:
        continue
    
    sldugeoid1 = feature1.GetField('sldu_geoid')
    sldlgeoid1 = feature1.GetField('sldl_geoid')
    uscdgeoid1 = feature1.GetField('uscd_geoid')
    sldugeoid2 = feature2.GetField('sldu_geoid')
    sldlgeoid2 = feature2.GetField('sldl_geoid')
    uscdgeoid2 = feature2.GetField('uscd_geoid')
    
    add_new_feature(out_lyr, geometry, sldugeoid1, sldlgeoid1, uscdgeoid1, sldugeoid2, sldlgeoid2, uscdgeoid2)
    
    count += 1
    if count == 16:
        pass # break

print(out_path, file=sys.stdout)
out_ds.Destroy()
