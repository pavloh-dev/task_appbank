import re

from pydantic import BaseModel, field_validator


class BankTransactionModel(BaseModel):
    account_id: str
    date: str
    description: str
    amount: float
    currency: str
    transaction_type: str

    @field_validator("date")
    def validate_date(cls, value: str):
        date_regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not date_regex.match(value):
            raise ValueError("Date must be in YYYY-MM-DD format")
        return value

    @field_validator("description")
    def validate_description(cls, value: str):
        if value == "":
            raise ValueError("Description must be non-empty")
        return value

    @field_validator("currency")
    def validate_currency(cls, value: str):
        allowed_currencies = ["USD", "EUR", "GBP", "JPY"]
        if value not in allowed_currencies:
            raise ValueError(f"Currency must be one of {allowed_currencies}")
        return value

    @field_validator("amount")
    def validate_amount(cls, value: float):
        if value < 0:
            raise ValueError("Amount must be positive.")
        return value

    @field_validator("transaction_type")
    def validate_transaction_type(cls, value: str):
        if value.lower() not in ["credit", "debit"]:
            raise ValueError("transaction_type must be either 'credit' or 'debit'")
        return value.lower()


class AccountModel(BaseModel):
    account_id: str
