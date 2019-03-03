import http.client
import json
import pandas
from pprint import pprint


connection = http.client.HTTPConnection('api.football-data.org')
headers = { 'X-Auth-Token': '901186e638fd4baa999bb2c32f4ef7d5' }
connection.request('GET', '/v2/competitions/PL/standings?standingType=HOME', None, headers )
response = json.loads(connection.getresponse().read().decode())
for item in response['standings'][0]['table']:
    print(f"{item['position']}. {item['team']['name']}")