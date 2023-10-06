import logging

from fastapi import FastAPI, HTTPException, Depends

from models.models import BankTransactionModel
from utils.business_logic import BankAccountService
from utils.datamodel import DataModel

logging.basicConfig(level=logging.INFO)

import logging


app = FastAPI()

logger = logging.getLogger("app")

bank_service = BankAccountService(AccountType="credit")
DataModel.init_db()


@app.post("/CreateAccount")
async def create_account(account_type: str, credit_limit: float = 0.0):
    logger.info("HEY")
    account_id = DataModel.create_account_db(account_type, credit_limit)
    if account_id is None:
        raise HTTPException(status_code=500, detail="Account creation failed.")
    return {"account_id": account_id}


@app.post("/{account_id}/ProcessTransaction")
async def process_transaction(
        transaction: BankTransactionModel,
        account: DataModel = Depends(DataModel.get_account)
):
    return await bank_service.process_transaction(transaction, account)


@app.get("/{account_id}/GetBalance")
async def get_balance(
        account: DataModel = Depends(DataModel.get_account)
):
    return {"balance": DataModel.get_balance_from_db(account)}


@app.get("/{account_id}/GetTransactions")
async def get_transactions(
        account: DataModel = Depends(DataModel.get_account)
):
    transactions = DataModel.get_transactions_db(account)
    if transactions is None:
        raise HTTPException(status_code=404, detail="Account not found.")
    return {"transactions": transactions}
