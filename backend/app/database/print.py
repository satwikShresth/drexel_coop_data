import sqlite3


def print_data_from_db(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = f'SELECT * FROM "{table_name}"'
    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    print(f"{' | '.join(columns)}")
    print('-' * (len(columns) * 15))
    for row in rows:
        print(f"{' | '.join(map(str, row))}")

    conn.close()


sqlite_db_path = './uscities.db'
table_name = 'uscities'

print_data_from_db(sqlite_db_path, table_name)
