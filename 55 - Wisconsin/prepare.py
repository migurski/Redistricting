#!/usr/bin/env python3
import sys, csv, itertools

latlon = lambda row: (row['Latitude'], row['Longitude'])

def main(filename):
    '''
    '''
    with open(filename) as file:
        input = csv.DictReader(file)
        fieldnames = input.fieldnames
        rows = sorted(input, key=latlon)

    fieldnames.insert(0, 'gid')
    fieldnames[fieldnames.index('ReportingUnit')] = 'ReportingUnits'
    output = csv.DictWriter(sys.stdout, fieldnames, dialect='excel')
    output.writeheader()
    
    latlons, total, gids = 0, 0, itertools.count()
    
    for _, group in itertools.groupby(rows, latlon):
        row = next(group)
        reporting_units = [row.pop('ReportingUnit')]
        total += 1
        latlons += 1
        
        for other in group:
            reporting_units.append(other['ReportingUnit'])
            total += 1
        
        row['gid'] = next(gids)
        row['ReportingUnits'] = ', '.join(reporting_units)
        output.writerow(row)
    
    #
    # Add some far-flung points for the Voronoi tesselation
    #
    blank = {key: None for key in fieldnames}
    blank.update(gid=next(gids), Latitude=53.50, Longitude=-90.02)
    output.writerow(blank)
    blank.update(gid=next(gids), Latitude=36.05, Longitude=-102.23)
    output.writerow(blank)
    blank.update(gid=next(gids), Latitude=34.11, Longitude=-77.10)
    output.writerow(blank)
    
    print('total:', total, 'in', latlons, 'points', file=sys.stderr)

if __name__ == '__main__':
    _, filename = sys.argv
    exit(main(filename))
