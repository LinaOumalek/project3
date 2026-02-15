import psycopg2
from psycopg2 import pool
from fastapi import HTTPException, status
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()
db_pool = pool.SimpleConnectionPool(
    1, 10,
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST")
)

def execute_query(query, values= (), fetch = False):
    conn = db_pool.getconn()
    try:

        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, values)

        if fetch:
            res = cur.fetchall()
        else:
            res = None
        
        conn.commit()
        cur.close()
        conn.close()

        return res
        
    except psycopg2.IntegrityError as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    finally:
        db_pool.putconn(conn)