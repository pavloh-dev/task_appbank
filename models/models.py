from pydantic import BaseModel


class BankTransactionModel(BaseModel):
    Date: str
    Description: str
    Amount: float
    Currency: str
