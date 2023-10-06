from fastapi import FastAPI, HTTPException, Body
from models.models import BankTransactionModel
from utils.business_logic import BankAccountService
from utils.datamodel import DataModel

app = FastAPI(debug=True)
bank_service = BankAccountService()


async def get_account(account_id: str):
    account = await DataModel.get_account(account_id)
    if account:
        return account
    raise HTTPException(status_code=404, detail="Account not found")


@app.post("/CreateAccount")
async def create_account(account_type: str = Body(..., embed=True), credit_limit: float = Body(0.0, embed=True)):
    account_id = await DataModel.create_account_db(account_type, credit_limit)
    if not account_id:
        raise HTTPException(status_code=500, detail="Account creation failed.")
    return {"account_id": account_id}


@app.post("/{account_id}/ProcessTransaction")
async def process_transaction(
        transaction: BankTransactionModel,
        account_id,
):
    account = await get_account(account_id)
    await bank_service.process_transaction(transaction, account)
    return await get_balance(account[0])


@app.get("/{account_id}/GetBalance")
async def get_balance(account_id: str):
    account = await get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found.")
    return {"balance": await bank_service.get_current_balance(account[0])}


@app.get("/{account_id}/GetTransactions")
async def get_transactions(account_id):
    account = await get_account(account_id)
    transactions = await bank_service.get_transactions_list(account[0])
    if not transactions:
        raise HTTPException(status_code=404, detail="No transactions found.")
    return {"transactions": transactions}
