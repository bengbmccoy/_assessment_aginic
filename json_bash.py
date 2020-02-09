
import pandas as pd
import json
from pandas.io.json import json_normalize

with open('new_data.json', 'r') as read_file:
    sample_json = json.load(read_file)


print('the sample JSON looks like below:')
print(json.dumps(sample_json, indent=4), '\n')
