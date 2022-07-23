import sqlite3
import json

#сохраняет список таблиц БД sqllite в Json файл

sql_data = dict()

with sqlite3.connect('db.sqlite') as sql_conn:
    curs = sql_conn.cursor()
    curs.execute('''SELECT name FROM sqlite_master
                    WHERE type='table';
                    ''')
    table_names = curs.fetchall()

    for i in table_names:
        curs.execute(f'''SELECT COUNT(*) FROM {i[0]}''')
        film_work_size = curs.fetchone()
        sql_data[i[0]] = film_work_size[0]

print(sql_data)

with open('sqllite_tables','w') as f:
    json.dump(sql_data, f)
