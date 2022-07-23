import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from tables import *


class SQLiteLoader(object):

    def __init__(self, connection):
        self.connection = connection

    def load_movies(self, batch, start_point, table):
        with self.connection as conn:
            conn.row_factory = sqlite3.Row
            data = list()
            curs = conn.cursor()
            curs.execute(f"""SELECT * FROM {table.name}
                             ORDER BY id
                             LIMIT {start_point}, {batch};""")
            sql_data = curs.fetchall()
            for row in sql_data:
                movie = sql_to_dataclass(table, row)
                print(movie)
                data.append(movie)
        return data


class PostgresSaver(object):

    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_all_data(self, data, table):
        psycopg2.extras.register_uuid()
        conn = self.pg_conn
        cur = conn.cursor()
        data_query = data_fromdataclass(table, data)
        pg_insert_query = pg_insert(table)
        cur.executemany(pg_insert_query, data_query)
        conn.commit()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection, table):
    """Основной метод загрузки данных из SQLite в Postgres"""
    batch = 100
    start_point = 0
    limit = table.size

    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    while start_point < limit:
        batch = batch_check(limit, start_point, batch)
        try:
            data = sqlite_loader.load_movies(batch, start_point, table)  # получаем данные из slqlite БД
            postgres_saver.save_all_data(data, table)  # передаем данные в psql
            print('успешно загружено записей: ', start_point+batch)
        except:
            print('Ошибка. Порядковый номер значения партии: ', start_point)
        start_point = start_point + batch


if __name__ == '__main__':
    dsl = {'dbname': 'movies_db', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as _connection:
        load_from_sqlite(sqlite_conn, _connection, table=film_work)
        load_from_sqlite(sqlite_conn, _connection, table=genre)
        load_from_sqlite(sqlite_conn, _connection, table=person)
        load_from_sqlite(sqlite_conn, _connection, table=genre_film_work)
        load_from_sqlite(sqlite_conn, _connection, table=person_film_work)