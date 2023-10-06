import sqlite3
from typing import List

from fastapi import HTTPException

from models.models import BankTransactionModel
from utils.datamodel import DataModel


class BankAccountService:

    def __init__(self, AccountType: str, CreditLimit: float = 0.0):
        self.account_id = None
        self.transactions = []
        self.balance = 0.0
        self.accountType = AccountType.lower()
        self.creditLimit = CreditLimit

    async def process_transaction(self, transaction: BankTransactionModel, account_id: DataModel):
        if self.account_id is None:
            self.account_id = account_id

        amount = abs(transaction.amount)

        if transaction.transaction_type.lower() == "debit":
            amount = -amount

        new_balance = self.balance + amount

        insufficient_funds_condition = (
                self.accountType == "debit" and new_balance < 0
        )
        credit_limit_exceeded_condition = (
                self.accountType == "credit" and new_balance < -self.creditLimit
        )

        if insufficient_funds_condition or (transaction.transaction_type.lower() == "debit" and new_balance < 0):
            raise HTTPException(status_code=400, detail="Insufficient funds in account.")
        elif credit_limit_exceeded_condition or not new_balance > 0:
            raise HTTPException(status_code=400, detail="Credit limit exceeded and balance cannot be negative.")

        try:
            DataModel.add_transaction(account_id, transaction.date, transaction.description,
                                      transaction.amount, transaction.currency, transaction.transaction_type)
        except sqlite3.Error as e:
            raise HTTPException(status_code=500,
                                detail=f"An error occurred while trying to save the transaction: {str(e)}")

        self.transactions.append(transaction)
        self.balance = new_balance

        return {"balance": self.balance}

    async def get_transactions_list(self) -> List[BankTransactionModel]:
        return self.transactions

    async def get_current_balance(self) -> float:
        return self.balance


class BankAccountManager:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_type: str, credit_limit: float = 0.0):
        new_account = BankAccountService(account_type, credit_limit)
        self.accounts[new_account.account_id] = new_account
        return new_account.account_id

    def get_account(self, account_id: str):
        return self.accounts.get(account_id)


account_manager = BankAccountManager()
