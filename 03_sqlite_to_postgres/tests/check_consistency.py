import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor


def sqllite_check(sqlite_conn):

    sql_data = dict()
    curs = sqlite_conn.cursor()
    curs.execute('''SELECT name FROM sqlite_master
                    WHERE type='table';
                    ''')
    table_names = curs.fetchall()

    for i in table_names:
        curs.execute(f'''SELECT COUNT(*) FROM {i[0]}''')
        film_work_size = curs.fetchone()
        sql_data[i[0]] = film_work_size[0]

    return sql_data


def pg_check(_connection):

    pg_data = dict()
    curs = _connection.cursor()
    curs.execute('''SELECT * FROM pg_tables
                        WHERE schemaname = 'content';
                        ''')
    table_names = curs.fetchall()
    for i in table_names:
        curs.execute(f'''SELECT COUNT(*) FROM content.{i[1]}''')
        film_work_size = curs.fetchone()
        pg_data[i[1]] = film_work_size[0]

    return pg_data

def check_consistency(sqlite_conn, _connection):

    sqllite_data = sqllite_check(sqlite_conn)
    pg_data = pg_check(_connection)

    assert sqllite_data == pg_data, 'количество таблиц/записей не совпадают:('
    print('таблицы и количество записей: ок')

if __name__ == '__main__':
    dsl = {'dbname': 'movies_db', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('D:\Program Files (x86)\PythonPractice\\new_admin_panel_sprint_1\\03_sqlite_to_postgres/db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as _connection:
        check_consistency(sqlite_conn, _connection)

