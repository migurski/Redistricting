#!/usr/bin/env python3
from urllib.request import urlopen
from xlrd import open_workbook
import os, tempfile, re, sys, csv

# Linked from http://www.sos.ca.gov/elections/prior-elections/statewide-election-results/general-election-november-8-2016/statement-vote/
url = 'http://elections.cdn.sos.ca.gov/sov/2016-general/sov/06-sov-summary.xls'

resp = urlopen(url)

if resp.status is not 200:
    raise RuntimeError('Bad status from {}: {}'.format(url, resp.status))

_, filename = tempfile.mkstemp(prefix='California-Results-', suffix='.xls')

with open(filename, 'wb') as file:
    file.write(resp.read())

workbook = open_workbook(filename)
sheet = workbook.sheet_by_index(0)

# collect results in a list even though they are in two parallel columns
rows = list()

for row in sheet.get_rows():
    rows.append(row[0:3])

for row in sheet.get_rows():
    rows.append(row[4:7])

office, geoid, results = None, None, list()

for (cell1, cell2, cell3) in rows:
    if (cell1.ctype, cell2.value, cell3.value) == (1, 'Votes', 'Percent'):
        office = cell1.value
        continue
    elif (cell1.ctype, cell2.ctype, cell2.ctype) == (0, 0, 0):
        office = None
        continue
    
    if office == 'President':
        geoid = '06'
    elif 'United States Representative' in office:
        district = re.search(r'\b\d+$', office).group(0)
        geoid = '06{:02d}'.format(int(district))
    else:
        geoid = ''
    
    match = re.match(r'^(.+?)(\*?)((, \w+)+| \(W\/I\))$', cell1.value)
    
    if not match:
        continue
    
    party_abbr = ', '.join(filter(None, [p.strip() for p in match.group(3).split(',')]))
    party_name = ''
    candidate = match.group(1)
    votes = int(cell2.value)
    percentage = float(re.sub('%', '', cell3.value))

    results.append({
        'year': 2016, 'geoid': geoid,
        'office': office, 'party abbr': party_abbr,
        'party name': party_name, 'candidate': candidate,
        'votes': votes, 'percentage': percentage
        })

os.unlink(filename)

output = csv.DictWriter(sys.stdout,
    ('year', 'geoid', 'office', 'party abbr', 'party name', 'candidate', 'votes', 'percentage'))

output.writeheader()

for result in results:
    if result['office'] == 'President' \
    or 'United States Representative' in result['office']:
        output.writerow(result)
