from fastapi import HTTPException

from models.models import BankTransactionModel


class BankAccountService:
    def __init__(self, AccountType: str, CreditLimit: float = 0.0):
        self.Transactions = []
        self.Balance = 0.0
        self.AccountType = AccountType
        self.CreditLimit = CreditLimit

    async def ProcessTransaction(self, transaction: BankTransactionModel):
        if transaction.Currency != "USD":
            transaction.Amount /= 2

        NewBalance = self.Balance + transaction.Amount
        if self.AccountType == "Debit" and NewBalance < 0:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        elif self.AccountType == "Credit" and NewBalance < -self.CreditLimit:
            raise HTTPException(status_code=400, detail="Credit limit exceeded")

        self.Transactions.append(transaction.dict())
        self.Balance = NewBalance
        return {"Balance": self.Balance}


account = BankAccountService(AccountType="Debit")

