import psycopg2
from psycopg2.sql import SQL
from functools import wraps
from flask import current_app

def connect_db(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        conn = psycopg2.connect(
            host=current_app.config.get("DB_HOST"),
            database=current_app.config.get("DB_NAME"),
            user=current_app.config.get("DB_USER"),
            password=current_app.config.get("DB_PASSWORD")
        )
        cursor = conn.cursor()
        kwargs.update({
            "cursor" : cursor
        })
        result = func(*args, **kwargs)
        cursor.close()
        conn.close()
        return result
    return _wrapper

@connect_db
def check(cursor = None):
    cursor.execute(SQL('SELECT * from public.user where username=\'{}\' and password=\'{}\';'.format("admin'--", 'lol')))
    result = cursor.fetchall()
    print('sqli?')
    for r in result:
        print(r)

    cursor.execute(SQL('SELECT * from public.user where username=\'{}\' and password=\'{}\';'.format("jayse", '2222')))
    result = cursor.fetchall()
    print('norm?')
    for r in result:
        print(r)

    return True
