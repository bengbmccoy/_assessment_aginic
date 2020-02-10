'''
Written by: Ben McCoy, Feb 2020

This script is part 2 of the data engineer assessment provided by Aginic.

This script will take command line arguments which give the filepath of an
existing JSON file, as well as a filepath for an output database file to be
stored.

The script will use sqlite3 to store the JSON in a sqlite database.

NOTE: the JOSN key 'group' is changed to 'group_type' in the SQLite database
as 'group' is functional SQL command.

'''

import json
import sqlite3
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('json_file', type=str,
                        help='input JSON filepath')
    parser.add_argument('-output_file', type=str,
                        help='name of output JSON file')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='prints progress of script')
    args = parser.parse_args()

    with open(args.json_file, 'r') as read_file:
        json_dict = json.load(read_file)

    if args.verbose:
        print('the sample JSON looks like below:')
        print(json.dumps(json_dict, indent=4), '\n')

    db_cols = []
    db_cols = remove_duplicates(get_db_cols(json_dict, db_cols))
    db_cols[db_cols.index('group')] = 'group_type'
    if args.verbose:
        print('The list of keys in the dictionary are:')
        print(db_cols, '\n')

    create_string = gen_create_string('test_db', db_cols)
    if args.verbose:
        print('the create string looks like below:')
        print(create_string, '\n')

    conn = sqlite3.connect('activities_db')
    c = conn.cursor()
    c.execute(create_string)

    metadata = json_dict['metadata']
    all_insert_strings = []
    for i in range(metadata['activities_count']):
        insert_string, insert_dict = gen_insert_string(metadata, json_dict['activities_data'][i])
        if args.verbose:
            print('the insert string looks like below:')
            print(insert_string, tuple(insert_dict.values()), '\n')
        c.execute(insert_string, tuple(insert_dict.values()))

    conn.commit()
    conn.close()

def gen_insert_string(metadata, actdata):
    '''This function takes a JSON ticket's metadata and an activities data dict
    and returns a string and dict that can be used for an sqlite insert
    statement.'''

    comb_dict = {**metadata, **actdata}
    insert_dict = {}
    insert_dict = get_key_val_pairs(comb_dict, insert_dict)

    columns = ', '.join(insert_dict.keys())
    placeholders = ', '.join('?' * len(insert_dict))
    sql = 'INSERT INTO test_db ({}) VALUES ({})'.format(columns, placeholders)
    return sql, insert_dict


def get_key_val_pairs(d, d_fill):
    '''This function takes a nested dictionary with keys and values (d) and a
    flat dictionary (d_fill) that is to be filled with each key-value pair
    the function returns the falt dictionary.'''

    for k, v in d.items():
        if isinstance(v, dict):
            get_key_val_pairs(v, d_fill)
        else:
            if k == 'group':
                d_fill['group_type'] = v
            else:
                d_fill[k] = v
    return d_fill


def gen_create_string(tablename, columns):
    '''This function takes a list and creates a string that can be used to
    generate a table in SQLite3'''

    return f"CREATE TABLE {scrub(tablename)} ({columns[0]} text" + (
            ", {} text"*(len(columns)-1)).format(*map(scrub,columns[1:])) + ")"

def scrub(string):
    '''A quick scrub to ensure no SQL injection, removes any non alphanumeric
    characters from string'''

    if '_' in string:
        return string
    else:
        return ''.join(chr for chr in string if chr.isalnum())

def get_db_cols(d, l):
    '''This function takes a dict and a list of known keys in the dict, the
    function runs through the values is the dict and if a value is a dict or
    list it access that level of the dict. If the values in the dict are not
    a list or dict the keys are stored in a list, which is returned.'''

    for k, v in d.items():
        if isinstance(v, dict):
            get_db_cols(v, l)
        elif isinstance(v, list):
            for i in range(len(v)):
                if isinstance(v[i], dict):
                    get_db_cols(v[i], l)
                else:
                    l.append(v[i])
        else:
            l.append(str(k))

    return l

def remove_duplicates(l):
    seen = set()
    seen_add = seen.add
    return [x for x in l if not (x in seen or seen_add(x))]

if __name__ == "__main__":
    main()
