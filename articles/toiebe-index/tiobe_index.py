import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd

languages = ['java','c','cplusplus','python','csharp','php',
'visual-basic-dotnet','javascript','delphi-object-pascal','go',
'perl','swift','ruby','assembly-language','r','visual-basic',
'matlab','objective-c','scratch', 'pl-sql']

URL = 'https://www.tiobe.com/tiobe-index/'

def get_tiobe_index(language):

    def get_data(match_obj):
        nonlocal data
        data = match_obj.group(1)

    r = requests.get(URL + language)
    bs = BeautifulSoup(r.text, 'html.parser')

    data = [script for script in bs.find_all('script') if "$('#container').highcharts" in str(script)]
    data = str(data[0])
    data = re.sub('\s+', '', data)
    re.sub("data:(.*)}]", get_data, data)
    data = re.sub("Date.UTC\(([0-9]{4}),([0-9]{1,2}),([0-9]{1,2})\)", '"\\1-\\2-\\3"', data)
    data = json.loads(data)
    df = pd.DataFrame(data)
    df.columns = ['date', 'ratings']
    df.to_csv(language + '.csv', index=False)

for language in languages:
    print(language)
    get_tiobe_index(language)
