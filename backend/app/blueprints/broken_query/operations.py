import psycopg2
from psycopg2 import sql
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
def sqli_query(username, password, cursor = None):
    cursor.execute(
        sql.SQL('SELECT * FROM public.user \
             WHERE username=\'{}\' and password=\'{}\';'\
             .format(username, password)
            )
        )
    result = cursor.fetchall()
    return result
