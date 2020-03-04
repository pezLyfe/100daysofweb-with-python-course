import json
from typing import List

from apistar import App, Route, types, validators
from apistar.http import JSONResponse

def _load_stock_data():
    with open('stock_data.json') as f:
        stocks = json.loads(f.read())
        return {stock["ID"]: stock for stock in stocks}


stocks = _load_stock_data()

VALID_EXCHANGES = set([stock["Exchange"]
                          for stock in stocks.values()])

VALID_INDUSTRIES = set([stock["Industry"]
                          for stock in stocks.values()])

EXCHANGE_NOT_FOUND = 'Exchange not found'

INDUSTRY_NOT_FOUND = 'Industry not found'

class Stock(types.Type):
    Exchange = validators.String(enum=list(VALID_EXCHANGES), allow_null=True)  # assign in POST
    Company = validators.String(max_length = 300, allow_null=True)
    Cap = validators.String(max_length=10, allow_null = True)
    Industry = validators.String(enum=list(VALID_INDUSTRIES), allow_null=True)
    Sector = validators.String(default='n/a', allow_null=True)
    Ticker = validators.String(max_length=40, default='', allow_null=True)
    ID = validators.Integer(allow_null=True)


def list_stocks() -> List[Stock]:
    return [Stock(stock[1]) for stock in sorted(stocks.items())]


def create_stock(stock: Stock) -> JSONResponse:
    stock_id = max(stocks.keys())+1
    stock.id = stock_id
    stocks[stock_id] = stock
    return JSONResponse(Stock(stock), status_code=201)


def get_stock(stock_id: int) -> JSONResponse:
    stock = stocks.get(stock_id)
    if not stock:
        error = {'error': STOCK_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    return JSONResponse(Stock(stock), status_code=200)

def update_stock(stock_id: int, stock: Stock) -> JSONResponse:
    if not stocks.get(stock_id):
        error = {'error': STOCK_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    stock.id = stock_id
    stocks[stock_id] = stock
    return JSONResponse(Stock(stock), status_code=200)

def change_exchange(stock_id: int, stock: Stock) -> JSONResponse:
    if not stocks.get(stock_id):
        error = {'error': STOCK_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    stock.id = stock_id
    if stocks[stock_id].Exchange == "NYSE":
        stocks[stock_id].Exchange = "NASDAQ"
    elif stocks[stock_id].Exchange == "NASDAQ":
        stocks[stock_id].Exchange = "NYSE"
    else:
        error = {'error' : EXCHANGE_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    stocks[stock_id] = stock
    return JSONResponse(Stock(stock), status_code=200)


def delete_stock(stock_id: int) -> JSONResponse:
    if not stocks.get(stock_id):
        error = {'error': STOCK_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    del stocks[stock_id]
    return JSONResponse({}, status_code=204)


routes = [
    Route('/', method='GET', handler=list_stocks),
    Route('/', method='POST', handler=create_stock),
    Route('/{stock_id}/', method='GET', handler=get_stock),
    Route('/{stock_id}/', method='PUT', handler=update_stock),
    Route('/{stock_id}/Exchange', method='PUT', handler=change_exchange),
    Route('/{stock_id}/', method='DELETE', handler=delete_stock),
]

app = App(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)

