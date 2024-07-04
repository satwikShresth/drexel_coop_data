import sqlite3

def get_sqlalchemy_schema(sqlite_path, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(sqlite_path)

    # Fetch the table schema using PRAGMA
    cursor = conn.execute(f'PRAGMA table_info({table_name})')
    columns = cursor.fetchall()
    print(columns)

    # Close the SQLite connection
    # conn.close()
    #
    # if not columns:
    #     print(f"Table {table_name} does not exist in the database.")
    #     return
    #
    # # Generate SQLAlchemy schema
    # column_defs = []
    # for col in columns:
    #     col_name = col[1]
    #     col_type = col[2]
    #     col_nullable = not col[3]
    #     col_primary_key = bool(col[5])
    #
    #     col_type_mapping = {
    #         "INTEGER": "Integer",
    #         "TEXT": "String",
    #         "BLOB": "LargeBinary",
    #         "REAL": "Float",
    #         "NUMERIC": "Numeric",
    #         # Add more SQLite to SQLAlchemy type mappings as needed
    #     }
    #
    #     col_type = col_type_mapping.get(col_type, "String")
    #     column_def = f"Column('{col_name}', {col_type}, nullable={
    #         col_nullable}, primary_key={col_primary_key})"
    #     column_defs.append(column_def)
    #
    # # Generate the final table definition
    # table_def = f"""
    # from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Numeric, LargeBinary
    #
    # metadata = MetaData()
    #
    # {table_name} = Table(
    #     '{table_name}', metadata,
    #     {',\n    '.join(column_defs)}
    # )
    # """
    # print(table_def)


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


sqlite_db_path = './../salary/database.db'
table_name = 'salary'

# print_data_from_db(sqlite_db_path, table_name)
get_sqlalchemy_schema(sqlite_db_path, table_name)
