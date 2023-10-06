import uuid
from sqlite3 import Row
from typing import Iterable

import aiosqlite
from fastapi import HTTPException


class DataModel:

    @staticmethod
    async def init_db():
        async with aiosqlite.connect('bank.db') as db:
            cursor = await db.cursor()
            await cursor.execute('''
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
            await db.commit()

    @staticmethod
    async def create_account_db(account_type: str, credit_limit: float = 0.0):
        account_id = str(uuid.uuid4())
        balance = 0.0
        async with aiosqlite.connect('bank.db') as db:
            cursor = await db.cursor()
            await cursor.execute('''
                INSERT INTO accounts (account_id, account_type, credit_limit, balance)
                VALUES (?, ?, ?, ?)
            ''', (account_id, account_type, credit_limit, balance))
            await db.commit()
            return account_id

    @staticmethod
    async def get_account(account_id: str):
        async with aiosqlite.connect('bank.db') as db:
            cursor = await db.cursor()
            await cursor.execute('SELECT * FROM accounts WHERE account_id = ?', (account_id,))
            account = await cursor.fetchone()
            if not account:
                raise HTTPException(status_code=404, detail="Account not found.")
            return account

    @staticmethod
    async def add_transaction(account_id, date: str, description: str, amount: float, currency: str,
                            transaction_type: str):
        async with aiosqlite.connect('bank.db') as db:
            async with db.cursor() as cursor:
                try:
                    await cursor.execute('BEGIN TRANSACTION')

                    await cursor.execute('''
                        INSERT INTO transactions (account_id, date, description, amount, currency, transaction_type)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (account_id, date, description,
                          amount, currency, transaction_type))

                    if transaction_type.lower() == 'debit':
                        new_amount = -abs(amount)
                    else:
                        new_amount = abs(amount)

                    await cursor.execute('''
                        UPDATE accounts
                        SET balance = balance + ?
                        WHERE account_id = ? AND balance + ? >= 0
                    ''', (new_amount, account_id, new_amount))

                    if cursor.rowcount == 0:
                        await cursor.execute('ROLLBACK')
                        raise HTTPException(status_code=400, detail="Insufficient funds or invalid transaction.")

                    await db.commit()

                    await cursor.execute('SELECT balance FROM accounts WHERE account_id = ?', (account_id,))
                    result = await cursor.fetchone()
                    return result[0] if result else None

                except Exception as e:
                    await cursor.execute('ROLLBACK')

                    if not isinstance(e, HTTPException):
                        raise HTTPException(status_code=500, detail=str(e))
                    else:
                        raise e

    @staticmethod
    async def get_balance_db(account_id) -> float:
        async with aiosqlite.connect('bank.db') as db:
            cursor = await db.cursor()
            await cursor.execute('SELECT balance FROM accounts WHERE account_id = ?', (account_id,))
            result = await cursor.fetchone()
            return result[0] if result else None

    @staticmethod
    async def get_transactions_db(account_id) -> Iterable[Row]:
        async with aiosqlite.connect('bank.db') as db:
            cursor = await db.cursor()
            await cursor.execute('SELECT * FROM transactions WHERE account_id = ?', (account_id,))
            return await cursor.fetchall()

