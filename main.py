from fastapi import FastAPI
import datetime

from models.models import BankTransactionModel
from utils.business_logic import account

app = FastAPI()


@app.post("/ProcessTransaction/")
async def CreateTransaction(transaction: BankTransactionModel):
    return await account.ProcessTransaction(transaction)


@app.get("/RetrieveBalance/")
async def RetrieveBalance(date: str = None):
    return {"Balance": account.Balance}


@app.get("/GetTransactions")
async def GetTransactions():
    QueriedTransactions = [
        trans for trans in account.Transactions
    ]
    return {"Transactions": QueriedTransactions}


@app.get("/QueryTransactions/")
async def QueryTransactions(startDate: str, endDate: str):
    StartDateObj = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    EndDateObj = datetime.datetime.strptime(endDate, "%Y-%m-%d")

    QueriedTransactions = [
        trans for trans in account.Transactions
        if StartDateObj <= datetime.datetime.strptime(trans["Date"], "%Y-%m-%d") <= EndDateObj
    ]
    return {"Transactions": QueriedTransactions}
