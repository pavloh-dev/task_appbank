import re

from pydantic import BaseModel, field_validator


class BankTransactionModel(BaseModel):
    date: str
    description: str
    amount: float
    currency: str

    @field_validator("date")
    def validate_date(cls, value):
        date_regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not date_regex.match(value):
            raise ValueError("Date must be in YYYY-MM-DD format")
        return value

    @field_validator("description")
    def validate_description(cls, value):
        if value == "":
            raise ValueError("Description must be non-empty")
        return value

    @field_validator("currency")
    def validate_currency(cls, value):
        allowed_currencies = ["USD", "EUR", "GBP", "JPY"]
        if value not in allowed_currencies:
            raise ValueError(f"Currency must be one of {allowed_currencies}")
        return value
