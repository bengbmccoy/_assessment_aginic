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
        print(json.dumps(sample_json, indent=4))
        print('')

    meta_fields = sample_json['metadata'].keys()
    print('metadata fields collected')
    print(meta_fields, '\n')

    activity_fields = sample_json['activities_data'][0].keys()
    print('activity fields collected')
    print(activity_fields, '\n')

    empty_activities = []
    for i in range(sample_json['metadata']['activities_count']):
        empty_activities.append(empty_dict(sample_json['activities_data'][i]['activity']))
    empty_activities = remove_duplicates(empty_activities)
    print('empty activity fields collected')
    print(empty_activities, '\n')

def empty_dict(d):
    '''Takes a nested python dict and sets all value to empty.'''
    for k, v in d.items():
        if isinstance(v, dict):
            empty_dict(v)
        else:
            d[k] = ''
    return d

def remove_duplicates(l):
    '''Takes a list and returns the unique value in the list
    this function was required as nested python dicts are not hashable and thus
    the function 'set' cannot be used on them.'''
    output = []
    for item in l:
        if item not in output:
            output.append(item)
    return output

if __name__ == "__main__":
    main()
