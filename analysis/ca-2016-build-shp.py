import glob, csv, tempfile, os, sys
from osgeo import ogr

with open('ca-2016/all_precinct_results.csv') as file:
    precincts = {row['pct16']: row for row in csv.DictReader(file)}
    print(sorted(precincts['001-356210'].keys()), file=sys.stderr)

out_path, out_ds, out_lyr = None, None, None

for input_path in glob.glob('ca-2016/shapefiles/*.shp'):
    print(input_path, '...', file=sys.stderr)
    input_ds = ogr.Open(input_path)
    input_lyr = input_ds.GetLayer(0)
    
    if out_ds is None:
        out_path = os.path.join(tempfile.mkdtemp(dir='.', prefix='ca-2016-'), 'precincts.shp')
        out_ds = ogr.GetDriverByName('ESRI Shapefile').CreateDataSource(out_path, ['ENCODING=UTF8'])
        out_lyr = out_ds.CreateLayer('things', input_lyr.GetSpatialRef(), ogr.wkbMultiPolygon)
        out_lyr.CreateField(ogr.FieldDefn('pct16', ogr.OFTString))
        out_lyr.CreateField(ogr.FieldDefn('area_km2', ogr.OFTReal))
        out_lyr.CreateField(ogr.FieldDefn('pres_blue', ogr.OFTInteger))
        out_lyr.CreateField(ogr.FieldDefn('pres_red', ogr.OFTInteger))
        out_lyr.CreateField(ogr.FieldDefn('sen_blue', ogr.OFTInteger))
        out_lyr.CreateField(ogr.FieldDefn('sen_red', ogr.OFTInteger))
        
    for input_feature in input_lyr:
        precinct_id = input_feature.GetField('pct16')
        precinct_row = precincts.get(precinct_id, {})
        input_area = input_feature.GetField('area')
    
        out_feature = ogr.Feature(out_lyr.GetLayerDefn())
        out_feature.SetGeometry(input_feature.GetGeometryRef())
        out_feature.SetField('pct16', precinct_id)
        out_feature.SetField('area_km2', (input_area / 1000000) if input_area else None)
        out_feature.SetField('pres_blue', precinct_row.get('pres_clinton'))
        out_feature.SetField('pres_red', precinct_row.get('pres_trump'))
        out_feature.SetField('sen_blue', precinct_row.get('ussenate_harris'))
        out_feature.SetField('sen_red', precinct_row.get('ussenate_sanchez'))
        out_lyr.CreateFeature(out_feature)

print(out_path, file=sys.stdout)
out_ds.Destroy()
