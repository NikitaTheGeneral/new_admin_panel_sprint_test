import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from movie_dataclasses import Movie, PG_test

class SQLiteLoader(object):

    def __init__(self, connection):
        self.connection = connection

    def load_movies(self):
        with self.connection as conn:
            conn.row_factory = sqlite3.Row
            data = list()
            curs = conn.cursor()
            curs.execute("""SELECT * FROM film_work
                             ORDER BY id
                             LIMIT 1, 5;""")
            sql_data = curs.fetchall()
            for i in sql_data:
                movie_row = i
                '''movie = Movie(title=movie_row['title'], description=movie_row['description'],
                              creation_date=movie_row['creation_date'], file_path=['file_path'], type=['type'],
                              rating=['rating'])'''
                movie = PG_test(name=movie_row['title'])
                data.append(movie)
        return data

class PostgresSaver(object):

    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_all_data(self, data):
        psycopg2.extras.register_uuid()
        conn = self.pg_conn
        cur = conn.cursor()
        data_query = list()
        for i in data:
            m = [i.id, i.name]
            data_query.append(m)
        print(data_query)
        pg_insert_query = """ INSERT INTO content.temp_table (id, name) 
                                                  VALUES (%s,%s) """
        cur.executemany(pg_insert_query, data_query)
        conn.commit()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_db', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as _connection:
        load_from_sqlite(sqlite_conn, _connection)
