import pytest
from fastapi import HTTPException

from utils.datamodel import DataModel


@pytest.mark.asyncio
async def test_create_account_db():
    account_id = await DataModel.create_account_db("Savings", 500.0)
    assert isinstance(account_id, str)


@pytest.mark.asyncio
async def test_get_account_failure():
    with pytest.raises(HTTPException):
        await DataModel.get_account("nonexistent_account_id")


@pytest.mark.asyncio
async def test_add_transaction_failure():
    with pytest.raises(HTTPException):
        await DataModel.add_transaction("nonexistent_account_id", "2023-10-10", "test", 100.0, "USD", "debit")


@pytest.mark.asyncio
async def test_get_balance_db(expected_balance=0):
    assert await DataModel.get_balance_db("test_account_id") == expected_balance


@pytest.mark.asyncio
async def test_get_transactions_db():
    transactions = await DataModel.get_transactions_db("test_account_id")
    assert isinstance(transactions, list)
