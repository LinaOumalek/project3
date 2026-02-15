from fastapi import FastAPI, status, HTTPException
from pydantic_models import UserModel
from helper import execute_query
import psycopg2
from pydantic_models import Account
from psycopg2.extras import RealDictCursor
import os
from psycopg2 import pool

db_pool = pool.SimpleConnectionPool(
    1, 10,
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST")
)


app = FastAPI()


@app.post("/users", status_code = status.HTTP_201_CREATED)
def create_user(user: UserModel):
    #business logic: valid email + valid phone
    
    query = "INSERT INTO users (full_name, email, phone) VALUES (%s, %s, %s)"
    values = (user.full_name, user.email, user.phone)
    execute_query(query, values)

    return {"status": "success", "data": user}

@app.post("/accounts", status_code = status.HTTP_201_CREATED)
def create_account(account: Account):
    query = "INSERT INTO accounts (user_id, currency) VALUES (%s, %s)"
    values = (account.user_id, account.currency)
    #business logic: user exists + valid currency
    execute_query(query, values)

    return {"status": "success", "data": account}


@app.post("/transactions/{account_id}", status_code= status.HTTP_200_OK)
def withdraw(account_id: int, amount: float):
    conn = db_pool.getconn()
    try:
        cur = conn.cursor(cursor_factory = RealDictCursor)
        query1 = cur.execute("SELECT balance, currency FROM accounts WHERE account_id = %s", (account_id, ))
        res1 = cur.fetchone()
        currency = res1["currency"]
        curr_balance = res1["balance"]

        if amount > curr_balance:
            raise HTTPException(status_code = 400, detail = "Insufficient Funds")

        cur.execute("INSERT INTO ledger (account_id, type, amount, currency) VALUES (%s,%s,%s,%s)", (account_id, "withdrawal", amount, currency))

        query3 = cur.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s RETURNING balance", (amount, account_id))
        res3 = cur.fetchone()

        return {"status": "success", "data": {"account_id": account_id, "balance": res3["balance"]}}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db_pool.putconn(conn)


@app.post("/transactions/transfers", status_code= status.HTTP_200_OK)
def transfer(account1_id: int, account2_id: int, amount: float):
    conn = db_pool.getconn()
    try:
        cur = conn.cursor(cursor_factory = RealDictCursor)
        cur.execute("SELECT balance, currency FROM accounts WHERE account_id = %s OR account_id =%s", (account1_id, account2_id))
        res = cur.fetchall()
        balance1, currency1 = res[0]["balance"], res[0]["currency"]
        balance2, currency2 = res[1]["balance"], res[1]["currency"]

        if balance1 <amount :
            raise HTTPException(status_code= 400, detail= "Insufficient funds")

        cur.execute("INSERT INTO ledger (account_id, type, amount, currency, related_account) VALUES (%s, %s,%s,%s,%s)",
                     (account1_id, "transfer", amount, currency1, account2_id))
        
        cur.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s RETURNING balance", (amount, account1_id))
        cur.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s RETURNING balance", (amount, account2_id))
        res1 = cur.fetchone()
        conn.commit()
        return {"status": "success", "data": res1["balance"]}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code = 500, details = str(e))
    finally:
        db_pool.putconn(conn)
