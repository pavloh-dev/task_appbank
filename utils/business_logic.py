from fastapi import HTTPException
from models.models import BankTransactionModel
from utils.datamodel import DataModel


class BankAccountService:

    async def process_transaction(self, transaction: BankTransactionModel, account):
        account_id, account_type, credit_limit, balance = account

        amount = abs(transaction.amount)
        if transaction.transaction_type.lower() == "debit":
            amount = -amount
        new_balance = balance + amount

        if account_type.lower() == "debit" and new_balance < 0:
            raise HTTPException(status_code=400, detail="Insufficient funds in account.")
        elif account_type.lower() == "credit" and new_balance < -credit_limit:
            raise HTTPException(status_code=400, detail="Credit limit exceeded.")

        await DataModel.add_transaction(account_id, transaction.date, transaction.description,
                                  transaction.amount, transaction.currency, transaction.transaction_type)

    async def get_transactions_list(self, account_id: str):
        return await DataModel.get_transactions_db(account_id)

    async def get_current_balance(self, account_id: str):
        return await DataModel.get_balance_db(account_id)
