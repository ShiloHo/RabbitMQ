#!/usr/bin/env python
import os
import sqlite3
"""Delete all test file and tables"""


sqlite_db_name = 'chinook.db'
sqlite_db_path = os.path.join(os.getcwd(),sqlite_db_name)
test_folder =  os.path.join(os.getcwd(),'tests')
drop_query = """SELECT 'DROP TABLE '|| name ||';' AS DROP_QUERY
           FROM SQLITE_MASTER
           WHERE TYPE = 'table'
           AND NAME LIKE 'test_%' ;"""

print( " Delete files from folder %r.." % test_folder)

for file_name in os.listdir(test_folder):
        file_path = os.path.join(test_folder, file_name)
        if os.path.isfile(file_path):
                 os.unlink(file_path)
                 print("  - file %r deleted " % file_name)

print( " Delete tables from db %r.." % sqlite_db_name)
with sqlite3.connect(sqlite_db_path) as connection_sqlite:
        cursor_sqlite = connection_sqlite.cursor()
        try:
            exec_d= cursor_sqlite.execute(drop_query)
            drop_list_q = exec_d.fetchall()
            for q in drop_list_q:
                drop_q = q[0]
                print("  - table %r deleted " % drop_q.strip("DROP TABLE ").strip(";") )
                cursor_sqlite.execute(drop_q)
        except sqlite3.OperationalError as e:
            print('Sqlite operational error: {}'.format(e))