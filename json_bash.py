
import pandas as pd
import json
from pandas.io.json import json_normalize

json_string = '''
{

"metadata": {

"start_at": "20-04-2017 10:00:00 +0000",

"end_at": "21-04-2017 09:59:59 +0000",

"activities_count": 2

},

"activities_data": [

{

"performed_at": "21-04-2017 09:33:38 +0000",

"ticket_id": 600,

"performer_type": "user",

"performer_id": 149018,

"activity": {

"note": {

"id": 4025864,

"type": 4

}

}

},

{

"performed_at": "21-04-2017 09:38:24 +0000",

"ticket_id": 704,

"performer_type": "user",

"performer_id": 149018,

"activity": {

"shipping_address": "N/A",

"shipment_date": "21 Apr, 2017",

"category": "Phone",

"contacted_customer": true,

"issue_type": "Incident",

"source": 3,

"status": "Open",

"priority": 4,

"group": "refund",

"agent_id": 149018,

"requester": 145423,

"product": "mobile"

}

}

]

}
'''

# data = json.loads(json_string)
# print(data['metadata'])
# print(data['activities_data'])

# for item in data:
#     print('  ')
#     print(item)
#     print(data[item])

    # for thing in data[item]:
    #     print('  ')
    #     print(thing)

# print(json_normalize(data).to_string())
# json_normalize(data).to_csv('testing.csv')
#
# train = pd.DataFrame.from_dict(data, orient='index')
# print(train.reset_index(level=0, inplace=True))

### SAVING A JSON ON DISK ###
# with open('data_file.json', 'w') as write_file:
#     json.dump(data, write_file)

# print(json.dumps(data, indent=4))

with open('data_file.json', 'r') as read_file:
    data = json.load(read_file)

# print(json.dumps(data, indent=4))

for activity_data in data['activities_data']:
    print(activity_data['activity'])
    print(' ')
    # for field in activity_data:
        # print(field)
    # print(' ')

# for thing in data['activities_data']['activity']:
    # print(thing)

# print(data['activities_data'])
