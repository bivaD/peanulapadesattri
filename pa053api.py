from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import requests

app = FastAPI()


def get_airport_temperature(airport_code):
    airport_url = f"https://www.airport-data.com/api/ap_info.json?iata={airport_code}"
    airport_response = requests.get(airport_url)
    airport_data = airport_response.json()
    
    latitude = airport_data.get('latitude')
    longitude = airport_data.get('longitude')
    
    if latitude is None or longitude is None:
        raise HTTPException(status_code=404, detail="Latitude or longitude data not found for the given airport code")
    
    weather_url = f"http://api.weatherapi.com/v1/current.json?key=7dbc2d10a3854351b4862623242904&q={latitude},{longitude}"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()
    
    temperature = weather_data.get('current', {}).get('temp_c')
    
    if temperature is None:
        raise HTTPException(status_code=404, detail="Temperature data not found for the given coordinates")
    
    return temperature

def get_stock_price(stock_code):
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes?region=US&symbols={stock_code}"
    headers = {
        'x-rapidapi-key': 'b2067eca84msh3325e30035425a3p12a11ajsn4863bb6d0d0d',
        'x-rapidapi-host': 'apidojo-yahoo-finance-v1.p.rapidapi.com'
    }
    response = requests.get(url, headers=headers)
    price = response.json()['quoteResponse']['result'][0]['regularMarketPrice']
    if price is None:
        raise HTTPException(status_code=404, detail="Stock price data not found for the given stock code")
    
    return price


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
            return temperature
        except HTTPException as e:
            raise e
    elif queryStockPrice:
        try:
            price = get_stock_price(queryStockPrice)
            return price
        except HTTPException as e:
            raise e
    elif queryEval:
        try:
            result = evaluate_expression(queryEval)
            return result
        except HTTPException as e:
            raise e
    else:
        raise HTTPException(status_code=400, detail="Exactly one query parameter must be provided")
