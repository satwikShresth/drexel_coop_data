import sqlite3


def print_data_from_db(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = f'''
    SELECT DISTINCT Company, Position, "Salary Per Hour"
    FROM "{table_name}"
    GROUP BY Company, Position, "Salary Per Hour"
    HAVING COUNT(*) = 1;
    '''

    # query = f'''
    # UPDATE {table_name}
    # SET Company = 'West Pharmaceutical Services'
    # WHERE Company LIKE 'West Pharma%';
    # '''
    # cursor.execute(query)
    # conn.commit()
    #
    # query = f'''
    # SELECT * FROM "{table_name}"
    # WHERE Company = 'West Pharmaceutical Services';
    # '''

    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    print(f"{' | '.join(columns)}")
    print('-' * (len(columns) * 15))
    for row in rows:
        print(f"{' | '.join(map(str, row))}")

    conn.close()


sqlite_db_path = './database.db'
table_name = 'salary'

print_data_from_db(sqlite_db_path, table_name)
