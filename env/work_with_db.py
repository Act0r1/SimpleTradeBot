import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)


    return conn


def create_table(conn, create_table_sql):
    """
    create table from create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:    
    
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    db = r'pythonsqlite.db'
    sql_bot_table = """
    CREATE TABLE IF NOT EXISTS bot(
        sell_or_buy text,
        ticket text,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        price INTEGER NOT NULL,
        GAP INTEGER NOT NULL
    )
    """

    conn = create_connection(db)


    if conn is not None:
        create_table(conn, sql_bot_table)
    
    else:
        print("Error! cannot create the database connection.")



if __name__ == "__main__":
    main()