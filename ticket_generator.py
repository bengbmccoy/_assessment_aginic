'''
Written by: Ben McCoy, Feb 2020

This script is written for the Aginic data engineer assessment tasks.

This script will take a sample JSON file with data regarding the activity
of a helpdesk system ticket software, as well as command line arguments which
define the number of randomly generated tickets and the output file location.

The script will load the sample JSON file and use it to create an empty
activities data template to be filled with random activity.

The script will then iterate through the number of tickets_gen, creating random
activities data to be added to a new JSON.

Finally, the meta data of the new JSON will be generated, with the start and
end datetimes to be filled after checking the activities data start and end
datetimes.

'''

import argparse
import json
import datetime
import random
import copy

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('sample_data', type=str,
                        help='sample JSON filepath')
    parser.add_argument('-ticket_gen', type=int, default=100,
                        help='number of tickets to generate, defualt is 100')
    parser.add_argument('-output_file', type=str,
                        help='name of output JSON file')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='prints progress of script')
    args = parser.parse_args()

    with open(args.sample_data, 'r') as read_file:
        sample_json = json.load(read_file)

    if args.verbose:
        print('the sample JSON looks like below:')
        print(json.dumps(sample_json, indent=4), '\n')

    meta_fields = sample_json['metadata'].keys()
    if args.verbose:
        print('metadata fields extracted:')
        print(meta_fields, '\n')

    activities_samples = []
    for i in range(sample_json['metadata']['activities_count']):
            activities_samples.append(sample_json['activities_data'][i])
    activities_samples = remove_duplicates(activities_samples)
    if args.verbose:
        print('activities samples extracted:')
        print(activities_samples, '\n')

    new_act_data = []
    for i in range(args.ticket_gen):
        rand_act = random.randint(0, sample_json['metadata']['activities_count']-1)
        empty_json = empty_dict(activities_samples[rand_act])
        new_activity = fill_empty_act_json(empty_json)
        new_act_data.append(copy.deepcopy(new_activity))
        if i % (args.ticket_gen/10) == 0:
            if args.verbose:
                print('The ' + str(i) + 'th new activity is: ', new_activity, '\n')

    new_metadata = fill_empty_metadata(meta_fields, new_act_data)
    if args.verbose:
        print('new metadata fields are filled in:')
        print(new_metadata, '\n')

    if args.output_file:
        new_json = dict()
        new_json['metadata'] = new_metadata
        new_json['activities_data'] = new_act_data

        with open(args.output_file, 'w') as fp:
            json.dump(new_json, fp)

        if args.verbose:
            print('the file has been saved as: ')
            print(args.output_file)

def fill_empty_metadata(meta_fields, act_list):
    '''This function take the keys of the metadata fields and a filled list
    of randomly generated activities and fills in the metadata required for
    the generated data.'''

    datetime_list=[]
    meta_dict = {}
    for i in range(len(act_list)):
        datetime_list.append(act_list[i]['performed_at'])
    meta_fields = list(meta_fields)
    meta_dict[meta_fields[0]] = min(datetime_list)
    meta_dict[meta_fields[1]] = max(datetime_list)
    meta_dict[meta_fields[2]] = len(datetime_list)
    return meta_dict

def fill_empty_act_json(json):
    '''Iterates through nested python dicts and when at the end of a nested
    structure, generates random data for activities data with empty values'''

    for k, v in json.items():
        if isinstance(v, dict):
            fill_empty_act_json(v)
        else:
            if v == '':
                json[k] = gen_value(k)
    return json

def gen_value(k):
    '''Takes a key from the json and returns a value that is randomly generated
    and matches the data from that key. Some keys will require the use of more
    complex functions to generate random values/datetimes.'''

    if k in ['performed_at', 'start_at', 'end_at']:
        val = gen_rand_datetime()
    elif k in ['ticket_id']:
        val = random.randint(100,999)
    elif k in ['agent_id', 'requester']:
        val = random.randint(100000, 999999)
    elif k in ['id']:
        val = random.randint(1000000, 9999999)
    elif k in ['shipment_date']:
        val = gen_rand_date()
    elif k in ['status']:
        val = gen_rand_status()
    return val

def gen_rand_status():
    '''Returns a random value out of Open, Closed, Resolved, Waiting for
    Customer, Waiting for Third Party, or Pending'''

    status_vals = ['Open', 'Closed', 'Resolved', 'Waiting for Customer',
    'Waiting for Third Party', 'Pending']
    return status_vals[random.randint(0,5)]

def gen_rand_date():
    '''Generates a random date between the date provided in the sample JSON
    and an arbitrary date 4 years in the future. Returns the date in the
    DD MMM YYY string format'''

    start = '20 Apr 2017'
    end = '20 Apr 2020'
    frmt = '%d %b %Y'
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    td = etime - stime
    return (random.random() * td + stime).strftime('%d %b %Y')

def gen_rand_datetime():
    '''Generates a random datetime between the date provided in the sample JSON
    and an arbitrary date 4 years in the future. Removes the decimals on the
    seconds, adds the timezone afterwards as a string'''

    start = '20-04-2017 10:00:00'
    end = '20-04-2020 10:00:00'
    frmt = '%d-%m-%Y %H:%M:%S'
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    td = etime - stime
    return str(random.random() * td + stime).split('.')[0] + ' +0000'

def empty_dict(d):
    '''Takes a nested python dict and sets values as empty if they are in
    'del fields'. '''

    del_fields = ['performed_at', 'ticket_id', 'id',
    'shipment_date', 'status', 'agent_id', 'requester']
    for k, v in d.items():
        if isinstance(v, dict):
            empty_dict(v)
        else:
            if k in del_fields:
                d[k] = ''
    return d

def remove_duplicates(l):
    '''Takes a list and returns the unique value in the list
    this function was required as nested python dicts are not hashable and thus
    the function 'set' cannot be used on them. '''

    output = []
    for item in l:
        if item not in output:
            output.append(item)
    return output

if __name__ == "__main__":
    main()
