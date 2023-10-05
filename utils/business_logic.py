from fastapi import HTTPException

from models.models import BankTransactionModel


class BankAccountService:
    def __init__(self, AccountType: str, CreditLimit: float = 0.0):
        self.transactions = []
        self.balance = 0.0
        self.accountType = AccountType
        self.creditLimit = CreditLimit

    async def ProcessTransaction(self, transaction: BankTransactionModel):
        if transaction.currency != "USD":
            transaction.amount /= 2

        NewBalance = self.balance + transaction.amount
        if self.accountType == "Debit" and NewBalance < 0:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        elif self.accountType == "Credit" and NewBalance < -self.creditLimit:
            raise HTTPException(status_code=400, detail="Credit limit exceeded")

        self.transactions.append(transaction)
        self.balance = NewBalance
        return {"Balance": self.balance}


account = BankAccountService(AccountType="Debit")

