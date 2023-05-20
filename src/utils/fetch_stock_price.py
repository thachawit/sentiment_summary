import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import pandas as pd


# get the stock price and put it in xlsx file
def put_the_stock_price_to_xlsx(symbol, start_date, end_date):
    symbol = input("Enter the stock symbol: ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    # Use the yfinance library to retrieve the stock data
    df = yf.download(symbol, start=start_date, end=end_date)

    # Save the data to an xlsx file
    df.to_excel(symbol + ".xlsx")

    print("Data saved to " + symbol + ".xlsx")


# plot the posts from twitter on the closing price graph to visualize the relationships
def plot_stock_price_with_dots(symbol, start_date, end_date, num_dots, dot_dates):
    """
    This function retrieves the stock data for a specified symbol and date range,
    and plots the daily closing prices along with red dots on specific dates.
    """
    # Use the yfinance library to retrieve the stock data
    df = yf.download(symbol, start=start_date, end=end_date)

    # Plot the close price over time
    plt.plot(df["Close"], label="Closing Price")

    # Convert dot_dates to datetime format
    dot_dates = pd.to_datetime(dot_dates)

    # Get the dates and prices for the red dots
    dots = []
    for dot_date in dot_dates:
        if dot_date in df.index:
            dot_price = df.loc[dot_date, "Close"]
            dots.append((dot_date, dot_price))

    # Add the red dots to the graph and label them with their dates
    for dot in dots:
        plt.scatter(dot[0], dot[1], c="red", s=100,
                    label=dot[0].strftime('%Y-%m-%d'))

    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.title("Closing Price of " + symbol)
    plt.legend()
    plt.show()
