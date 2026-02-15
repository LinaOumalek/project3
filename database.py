import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(dbname = os.getenv("DB_NAME"), user = os.getenv("DB_USER"), password = os.getenv("DB_PASSWORD"))
cur = conn.cursor()

#User Table
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            
            )

""")

#Accounts Table
cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
            account_id SERIAL PRIMARY KEY,
            user_id INT,
            currency VARCHAR(3) NOT NULL,
            balance NUMERIC(15,2) DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_accountsToUsers FOREIGN KEY (user_id) REFERENCES users(user_id)
            )

""")

#Ledger Table
cur.execute("""
    CREATE TABLE IF NOT EXISTS ledger (
           ledger_id SERIAL PRIMARY KEY,
            account_id INT,
            type TEXT NOT NULL,
            amount NUMERIC(15,2) NOT NULL,
            currency VARCHAR(3) NOT NULL,
            related_account INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'completed',
            CONSTRAINT fk_ledgerToAccount FOREIGN KEY (account_id) REFERENCES accounts(account_id),
            CONSTRAINT fk_ledgerToAccount2 FOREIGN KEY (related_account) REFERENCES accounts(account_id)

            )

""")

conn.commit()