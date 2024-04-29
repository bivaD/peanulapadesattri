from fastapi import FastAPI, HTTPException, Query
import requests

app = FastAPI()

# Function to get temperature of a given airport
def get_airport_temperature(airport_code):
    url = f"http://www.airport-data.com/api/v1/getWeather.php?icao={airport_code}"
    response = requests.get(url)
    data = response.json()
    temperature = data.get('temperature', None)
    if temperature is None:
        raise HTTPException(status_code=404, detail="Temperature data not found for the given airport code")
    return temperature

# Function to get stock price of a given stock
def get_stock_price(stock_code):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes?region=US&symbols={stock_code}"
    headers = {
        'x-rapidapi-key': 'your-rapidapi-key',
        'x-rapidapi-host': 'apidojo-yahoo-finance-v1.p.rapidapi.com'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    price = data.get('quoteResponse', {}).get('result', [])[0].get('regularMarketPrice', None)
    if price is None:
        raise HTTPException(status_code=404, detail="Stock price data not found for the given stock code")
    return price

# Function to evaluate arithmetic expression
def evaluate_expression(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid arithmetic expression")

@app.get("/")
async def root(
    queryAirportTemp: str = Query(None, alias="queryAirportTemp"),
    queryStockPrice: str = Query(None, alias="queryStockPrice"),
    queryEval: str = Query(None, alias="queryEval")
):
    if queryAirportTemp:
        try:
            temperature = get_airport_temperature(queryAirportTemp)
            return {"temperature": temperature}
        except HTTPException as e:
            raise e
    elif queryStockPrice:
        try:
            price = get_stock_price(queryStockPrice)
            return {"price": price}
        except HTTPException as e:
            raise e
    elif queryEval:
        try:
            result = evaluate_expression(queryEval)
            return {"result": result}
        except HTTPException as e:
            raise e
    else:
        raise HTTPException(status_code=400, detail="Exactly one query parameter must be provided")
