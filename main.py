import math
import yfinance as yf
import csv
from stockList import stockList
from datetime import date

stockFinancialResults = []

# loops through watchlist and passes in stock to getSymbol function


def stocksInList():
    for stock in stockList:
        getStockInformation(stock)


# gets stocks symbol from watchList array
def getStockInformation(stock):
    for key, value in stock.items():
        stockInfoRequest(key, value['Ticker'], value['Target Price'])


# web scrap from yahoo to get prices
def stockInfoRequest(stockName, ticker, targetPrice):
    current_stock = yf.Ticker(ticker)
    current_stock_info = current_stock.info

    stock_name = current_stock_info["shortName"]
    symbol = current_stock_info["symbol"]
    sector = current_stock_info["sector"]
    currency = current_stock_info["currency"]
    open_price = current_stock_info["open"]
    current_price = current_stock_info["currentPrice"]
    previous_close_price = current_stock_info["previousClose"]
    volume = current_stock_info["volume"]
    div_rate = current_stock_info["dividendRate"]
    div_yield = round((current_stock_info["dividendYield"]) * 100, 2)

    div_date = current_stock_info["exDividendDate"]
    formatted_div_date = date.fromtimestamp(div_date)

    beta = round(current_stock_info["beta"], 2)
    pe_ratio = round(current_stock_info["trailingPE"], 2)

    market_cap = current_stock_info["marketCap"]
    # formats market cap
    millnames = ['', ' Thousand', ' Million', ' Billion', ' Trillion']
    millidx = max(0, min(len(millnames)-1,
                         int(math.floor(0 if market_cap == 0 else math.log10(abs(market_cap))/3))))
    formatted_market_cap = '{:.0f}{}'.format(
        market_cap / 10**(3 * millidx), millnames[millidx])

    fifty_two_week_low = current_stock_info["fiftyTwoWeekLow"]
    fifty_two_week_high = current_stock_info["fiftyTwoWeekHigh"]
    year_target_price_est = current_stock_info["targetMeanPrice"]

    stock_history = current_stock.history(period="max")
    highest_hist_price = round(max(stock_history["High"]), 2)


    stockResultsCompile(stock_name, symbol, sector, currency, open_price,
                        current_price, previous_close_price, volume, div_rate, div_yield,
                        formatted_div_date, beta, pe_ratio, formatted_market_cap,
                        fifty_two_week_low, fifty_two_week_high, year_target_price_est, highest_hist_price
                        )


#  function appends stock information to a results array
def stockResultsCompile(stock_name, symbol, sector, currency, open_price,
                        current_price, previous_close_price, volume, div_rate, div_yield,
                        formatted_div_date, beta, pe_ratio, formatted_market_cap,
                        fifty_two_week_low, fifty_two_week_high, year_target_price_est, highest_hist_price):


    price_difference = round(highest_hist_price - current_price,2)

    # look into buying the stock when it drops below entry price
    suggested_entry_price = round(.75 * highest_hist_price,2)
    print("Entry Price", suggested_entry_price)

    # indicate whether to buy or wait
    if current_price > suggested_entry_price:
        indicator = "Wait To Buy"
    else:
        indicator = "Buy Now"

    print("Indicator", indicator)

    stockFinancialResults.append({"Stock Name": stock_name,
                                  "Symbol": symbol,
                                  "Sector": sector,
                                  "Currency":currency ,
                                  "Open Price":open_price,
                                  "Current Price":current_price,
                                  "Previous Close Price":previous_close_price,
                                  "Volume": volume,
                                  "Dividend Rate": div_rate,
                                  "Dividend Yield": div_yield,
                                  "Divididend Date":formatted_div_date,
                                  "Beta": beta,
                                  "PE Ratio": pe_ratio,
                                  "Market Cap": market_cap,
                                  "52 Week Low": fifty_two_week_low,
                                  "52 Week High": fifty_two_week_high,
                                  "1y Target Estimate": year_target_price_est,
                                  "Suggested Entry Price": suggested_entry_price,
                                  "Price Difference": price_difference,
                                  "Wait/Buy Now": indicator})
    # createCsvFile()


# gets information from stockFinancialResults array to create csv file
def createCsvFile():

    today = str(date.today())
    fileNameFormat = "stock-watchlist-" + today + ".csv"

    with open(f'{fileNameFormat}', mode='w', newline='', encoding="utf-8-sig") as csvfile:
        fieldnames = ['Stock Name', 'Ticker', 'Beta', 'PE Ratio', 'Dividend Yield', '1y Target Estimate', 'Current Price',
                      'Target Entry Price', 'Price Difference', 'Wait/Buy Now']
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        # prints out the data from the stock Financial Results
        for stock in stockFinancialResults:
            writer.writerow(stock)


stocksInList()
# print(stockFinancialResults)
# print("File has been successfully created!")


# ADD CURRENT DATE AND TIME TO CSV FILE
