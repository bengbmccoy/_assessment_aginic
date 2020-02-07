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
    parser.add_argument('-output_file', type=str,
                        help='name of output JSON file')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='prints progress of script')
    args = parser.parse_args()

    with open(args.sample_data, 'r') as read_file:
        sample_json = json.load(read_file)

    if args.verbose:
        print(json.dumps(sample_json, indent=4))

    

if __name__ == "__main__":
    main()
