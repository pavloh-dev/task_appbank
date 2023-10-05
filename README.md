## Prerequisites 
Installation packages:
```shell
pip install -r requirements.txt
```

## Run the Bank Application

```sh
uvicorn main:app --reload
```

## API Endpoints

Access http://127.0.0.1:8000 to hit endpoints

### `POST /ProcessTransaction`
Submit a new transaction and update account balance. 
Required fields:
- `Date`: (string) Transaction date
- `Description`: (string) Transaction description
- `Amount`: (float) Transaction amount, use negative for outgoing transactions
- `Currency`: (string) Currency code (in our case - USD)


### `GET /GetTransactions`
Retrieve the list of all provided transactions.

it should look like this

![Transaction Screenshot](tran_1.png)

### `GET /RetrieveBalance`
Retrieve the current account balance.

### `GET /QueryTransactions`
Fetch transactions within a specified date range. 
Parameters:
- `startDate`: (string) Start date of the range
- `endDate`: (string) End date of the range
