#!/usr/bin/env python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re, csv, sys

# Linked from http://www.michigan.gov/sos/0,4670,7-127-1633_8722---,00.html
url = 'http://miboecfr.nictusa.com/election/results/2016GEN_CENR.html'

resp = urlopen(url)

if resp.status is not 200:
    raise RuntimeError('Bad status from {}: {}'.format(url, resp.status))

soup = BeautifulSoup(resp.read(), 'html.parser')
headers = [td.find_parent('tr') for td in soup.find_all('td', class_='offhdr')]
seen_rows = {None}
results = list()

for header in reversed(headers):
    office = header.find('td').text
    row = header

    while True:
        row = row.find_next('tr', class_=re.compile(r'^trow'))

        if row in seen_rows:
            break
        
        seen_rows.add(row)
        cells = row.find_all('td')
        party_abbr = cells[0].find('div', class_='abbr').text
        party_name = cells[0].find('div', class_='long').text
        candidate = cells[1].text
        votes = int(re.sub(',', '', cells[2].text))
        percentage = float(re.sub('%', '', cells[3].text))
        
        if 'President of the United States' in office:
            geoid = '26'
        elif 'District Representative in Congress' in office:
            district = re.search(r'^\d+', office).group(0)
            geoid = '26{:02d}'.format(int(district))
        else:
            geoid = ''

        results.append({
            'year': 2016, 'geoid': geoid,
            'office': office, 'party abbr': party_abbr,
            'party name': party_name, 'candidate': candidate,
            'votes': votes, 'percentage': percentage
            })

output = csv.DictWriter(sys.stdout,
    ('year', 'geoid', 'office', 'party abbr', 'party name', 'candidate', 'votes', 'percentage'))

output.writeheader()

for result in results:
    if 'President of the United States' in result['office'] \
    or 'District Representative in Congress' in result['office']:
        output.writerow(result)
