import sqlite3
import uuid
from contextlib import contextmanager
from typing import List, Tuple

from fastapi import HTTPException


@contextmanager
def get_db_connection():
    connection = sqlite3.connect("bank.db")
    try:
        yield connection
    finally:
        connection.close()


@contextmanager
def get_db_cursor(connection):
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        cursor.close()


class DataModel:

    @staticmethod
    def init_db():
        try:
            with get_db_connection() as connection, get_db_cursor(connection) as cursor:
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY,
                    account_id TEXT,
                    date TEXT,
                    description TEXT,
                    amount REAL,
                    currency TEXT,
                    transaction_type TEXT
                )
                ''')
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id TEXT PRIMARY KEY,
                    account_type TEXT,
                    credit_limit REAL,
                    balance REAL
                )
                ''')
                connection.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

    @staticmethod
    def create_account_db(account_type: str, credit_limit: float = 0.0):
        account_id = str(uuid.uuid4())
        balance = 0.0
        with get_db_connection() as connection, get_db_cursor(connection) as cursor:
            cursor.execute('''
            INSERT INTO accounts (account_id, account_type, credit_limit, balance)
            VALUES (?, ?, ?, ?)
            ''', (account_id, account_type, credit_limit, balance))
            connection.commit()
            return account_id

    @staticmethod
    def get_account(account_id: str):
        with get_db_connection() as connection, get_db_cursor(connection) as cursor:

            cursor.execute('''
            SELECT * FROM accounts WHERE account_id = ?
            ''', (account_id,))
            account = cursor.fetchone()
            connection.close()
            if not account:
                raise HTTPException(status_code=404, detail="Account not found.")
            return account

    @staticmethod
    def add_transaction(account_id, date: str, description: str, amount: float, currency: str,
                        transaction_type: str):
        with get_db_connection() as connection, get_db_cursor(connection) as cursor:
            cursor.execute('''
            INSERT INTO transactions (account_id, date, description, amount, currency, transaction_type)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (account_id, date, description, amount, currency, transaction_type))
            connection.commit()

    @staticmethod
    def get_balance_from_db(account_id) -> float:
        with get_db_connection() as connection, get_db_cursor(connection) as cursor:
            cursor.execute('''
            SELECT balance FROM accounts WHERE account_id = ?
            ''', (account_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    @staticmethod
    def get_transactions_db(account_id) -> List[Tuple]:
        with get_db_connection() as connection, get_db_cursor(connection) as cursor:
            cursor.execute('SELECT * FROM transactions WHERE account_id = ?', (account_id,))
            return cursor.fetchall()

    @staticmethod
    def get_balance_db(account_id) -> float:
        with get_db_connection() as connection, get_db_cursor(connection) as cursor:
            cursor.execute('''
            SELECT balance FROM accounts WHERE account_id = ?
            ''', (account_id,))
            balance = cursor.fetchone()
            return balance[0] if balance else None
