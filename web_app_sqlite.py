import sqlite3
from sqlite3 import Error
import sys

# ================================== CONNECTION =====================================
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
# ================================== CONNECTION =====================================

# ================================ TABLE CREATION ===================================
sql_create_primary_table = """ CREATE TABLE IF NOT EXISTS primary_table (
                                    id integer PRIMARY KEY,
                                    field1 text NOT NULL,
                                    field2 text,
                                    field3 text
                                ); """

sql_create_secondary_table = """CREATE TABLE IF NOT EXISTS secondary_table (
                                id integer PRIMARY KEY,
                                a text NOT NULL,
                                b integer,
                                c integer NOT NULL,
                                d integer NOT NULL,
                                e text NOT NULL,
                                f text NOT NULL,
                                FOREIGN KEY (d) REFERENCES primary_table (id)
                            );"""

# create_table_sql takes in param from samples like above
# create_table(conn, sql_create_secondary_entrys_table)
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
# ================================ TABLE CREATION ===================================

# ================================== INSERTION ======================================
# Insert into main table
def create_primary_entry(conn, project):
    sql = ''' INSERT INTO primary_table (field1,field2,field3)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid

# Insert into secondary table
def create_secondary_entry(conn, task):
    sql = ''' INSERT INTO secondary_table (a,b,c,d,e,f)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    return cur.lastrowid
# ================================== INSERTION ======================================

def main():
    database = "test_db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        create_table(conn, sql_create_primary_table)
        create_table(conn, sql_create_secondary_table)

        # create a primary
        project = ('','','');
        primary_id = create_primary_entry(conn, project)
        # Primary ID comes from when the primary entry is created

        task_2 = ('', 1, 1, primary_id, '', '')

        # create a secondary
        create_secondary_entry(conn, task_1)
        create_secondary_entry(conn, task_2)


if __name__ == '__main__':
    main()
