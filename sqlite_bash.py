import sqlite3
import json

def main():

    #
    # employee_data = {'first': 'Josh', 'last': 'Doe', 'pay': 1000000}
    #
    # # create_connection('db_test.db')
    #
    # conn = sqlite3.connect('db_test.db')
    # c = conn.cursor()
    #
    # # creates new table with columns first, last and pay
    # c.execute('''CREATE TABLE employees (
    #             first text,
    #             last text,
    #             pay integer
    #             )''')
    #
    # # inserts new data into db
    # c.execute("INSERT INTO employees VALUES ('Mary', 'John', 60000)")
    # c.execute("INSERT INTO employees VALUES (:first, :last, :pay)",
    # {'first': employee_data['first'], 'last': employee_data['last'], 'pay': employee_data['pay']})
    # conn.commit()
    #
    # # Collects all data where the last name is 'Schafer'
    # # c.execute("SELECT * FROM employees WHERE last='Doe'")
    # c.execute("SELECT * FROM employees WHERE last=:last", {'last': 'Doe'})
    #
    # # Prints the results of the query above
    # print(c.fetchall())
    #
    # conn.commit()
    # conn.close()


    conn = sqlite3.connect('activities_db')
    c = conn.cursor()
    c.execute("SELECT * FROM test_db")
    print(c.fetchall())
    c.execute('select * from test_db')
    names = list(map(lambda x: x[0], c.description))
    print(names)
    print(c.fetchall())


def insert_emp(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES (:first, :last, :pay)",
        {'first': emp['first'], 'last': emp['last'], 'pay': emp['pay']})


def create_connection(db_file):
    '''creates a new connection to a sqlite database'''

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    main()
