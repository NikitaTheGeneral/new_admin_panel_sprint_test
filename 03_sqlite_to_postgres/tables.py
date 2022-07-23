import json
from movie_dataclasses import Filmwork, Genre, Person, Genre_film_work, Person_film_work

class Table(object):

    def __init__(self, name, size):
        self.name = name
        self.size = size

with open('sqllite_tables','r') as f:
    tables_size = json.load(f)

film_work = Table('film_work', tables_size['film_work'])
genre = Table('genre', tables_size['genre'])
person = Table('person', tables_size['person'])
genre_film_work = Table('genre_film_work', tables_size['genre_film_work'])
person_film_work = Table('person_film_work', tables_size['person_film_work'])

def sql_to_dataclass(table, row):
    if table == film_work:
        movie = Filmwork(title=row['title'], description=row['description'],
                              creation_date=row['creation_date'], file_path=row['file_path'], type=row['type'],
                              rating=row['rating'], id=row['id'])
    elif table == genre:
        movie = Genre(name=row['name'], description=row['description'], id=row['id'])
    elif table == person:
        movie = Person(full_name=row['full_name'], id=row['id'])
    elif table == genre_film_work:
        movie = Genre_film_work(film_work_id=row['film_work_id'], genre_id=row['genre_id'], id=row['id'])
    elif table == person_film_work:
        movie = Person_film_work(role=row['role'], film_work_id=row['film_work_id'], person_id=row['person_id'], id=row['id'])
    return movie

def pg_insert(table):
    if table == film_work:
        pg_insert_query = """ INSERT INTO content.film_work (id, title, description, creation_date, rating, type, created) 
                                VALUES (%s,%s,%s,%s,%s,%s, NOW())
                                ON CONFLICT (id) DO NOTHING; """
    elif table == genre:
        pg_insert_query = """ INSERT INTO content.genre (id, name, description, created) 
                                VALUES (%s,%s,%s, NOW())
                                ON CONFLICT (id) DO NOTHING; """
    elif table == person:
        pg_insert_query = """ INSERT INTO content.person (id, full_name, created) 
                                VALUES (%s,%s, NOW())
                                ON CONFLICT (id) DO NOTHING; """
    elif table == genre_film_work:
        pg_insert_query = """ INSERT INTO content.genre_film_work (id, film_work_id, genre_id, created) 
                                VALUES (%s,%s,%s, NOW())
                                ON CONFLICT (id) DO NOTHING; """
    elif table == person_film_work:
        pg_insert_query = """ INSERT INTO content.person_film_work (id, film_work_id, person_id, role, created) 
                                VALUES (%s,%s,%s, %s, NOW())
                                ON CONFLICT (id) DO NOTHING; """
    return pg_insert_query

def data_fromdataclass(table, data):
    """преобразовываем список датаклассов в список списков"""
    data_query = list()
    if table == film_work:
        for i in data:
            m = [i.id, i.title, i.description, i.creation_date, i.rating, i.type]
            data_query.append(m)
    if table == genre:
        for i in data:
            m = [i.id, i.name, i.description]
            data_query.append(m)
    if table == person:
        for i in data:
            m = [i.id, i.full_name]
            data_query.append(m)
    if table == genre_film_work:
        for i in data:
            m = [i.id, i.film_work_id, i.genre_id]
            data_query.append(m)
    if table == person_film_work:
        for i in data:
            m = [i.id, i.film_work_id, i.person_id, i.role]
            data_query.append(m)
    return data_query

def batch_check(limit, start_point, batch):
    """Метод проверки размера получаемой-загружаемой партии строк в таблицу"""
    if (limit - (start_point + batch)) < 0:
        batch = limit - start_point
        return batch
    else:
        return batch