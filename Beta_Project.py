# Import the needed libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime, timedelta
import yfinance as yf
from sklearn.linear_model import LinearRegression

# Now define our functions
def get_stock_tickers(allowed_tickers):
  """
  Ask the user to input stock tickers to include in an analysis.
  
  Returns:
  - list: List of valid stock tickers in string format.
  """

  # Initialize an empty list to store user-selected tickers
  selected_tickers = []

  print(f"{len(allowed_tickers)} Stock Tickers available for analysis: {allowed_tickers}\n")
  print("Please enter at least two ticker to include in the analysis.")
  while True:
    # Get user input for stock ticker
    ticker = input(
        "Enter a stock ticker to include in the analysis (or 'done' to finish): "
    ).upper()
    
    
    if ticker == 'DONE':
      if len(selected_tickers) < 2 :
        print("Please select more tickers\n")
      else:
        break
    elif ticker in selected_tickers:
      print(f"{ticker} is already part of your list. Please select a different one\n")
    elif ticker in allowed_tickers:
      selected_tickers.append(ticker)
      print(f"{ticker} added to the list\n")
    else:
      print(
          f"Warning: {ticker} is not available for analysis. Please enter another valid stock ticker or enter 'done'.\n"
      )

  return selected_tickers


def user_input_find_weekday():
  """
  Get user input for the number of weekdays he/she want to look at and return the corresponding date.

  Returns:
  - str: The date of the weekday x weekdays ago in 'YYYY-MM-DD' format the user specified.
  """
  while True:
    try:
      # Get user input for the number of weekdays
      x = int(
          input(
              "Enter the number of weekdays you want to include in the analysis from now into the past. Please note: to have represenative data include at least 10 days : "
          ))

      # Validate input
      if x <= 0:
        raise ValueError("Please enter a positive integer.")
      elif x > 7500:
        raise ValueError("Please enter a number less than 7,500.")

      # Call the function to find the weekday x weekdays ago
      result_date = find_weekday_x_days_ago(x)

      print(
          f"\nAll weekdays from {result_date} until yesterday will be used in the analysis"
      )
      return result_date
      break

    # Use error handling to catch invalid inputs
    except ValueError as e:
      print(f"Error: {e}")
      print("Please try again and insert an integer.")


def find_weekday_x_days_ago(x):
  """
  Find the date of the weekday that occurred x weekdays ago.
  
  Parameters:
  - x (int): The number of weekdays ago.
  
  Returns:
  - str: The date of the weekday x weekdays ago in 'YYYY-MM-DD' format.
  """
  # Get today's date
  today = datetime.now() - timedelta(days=1)

  # Initialize a counter for weekdays
  weekdays_found = 0

  # Loop backward from today to find the x weekdays ago
  while weekdays_found < x:
    today -= timedelta(days=1)
    # Check if the day currently checking is a weekday (Monday to Friday)
    if today.weekday() < 5:
      weekdays_found += 1

  return today.strftime('%Y-%m-%d')


# Function to get the adjusted Close Data
def import_adj_close_data(stocks, start_date, end_date):
  """
  Import the data of the selected stock tickers and extract the adjusted closing date.
  
  Parameters:
  - stocks (List): List of stock tickers to include in the analysis.
  - start_date (str): String with inputted weekdays in the past.
  - end_date (str): String with today's date.

  Returns:
  - pd.DataFrame: DataFrame with the selected tickers and start and end dates.
  """
  data_df = yf.download(stocks, start_date, end_date)
  return data_df["Adj Close"]


# Function to calculate daily returns
def calc_daily_returns(prices_df):
  """
  Calculate daily returns for each stock in the given DataFrame.

  Parameters:
  - prices_df (pd.DataFrame): DataFrame with adjusted closing prices of stocks.

  Returns:
  - pd.DataFrame: DataFrame with daily returns for each stock in percent.
  """

  # Calculate percentage change for each column (stock)
  daily_returns_df = prices_df.pct_change()

  # Drop the first row since it will have NaN value (no previous day)
  daily_returns_df = daily_returns_df.dropna()

  return daily_returns_df


def align_dataframes(df1, df2):
  """
  Trim the top rows of the larger DataFrame (or Series) until they are of the same length.
  Remove rows with NaN values in either DataFrame.

  Parameters:
  - df1 (pd.DataFrame): The first DataFrame.
  - df2 (pd.DataFrame): The second DataFrame.

  Returns:
  - pd.DataFrame, pd.DataFrame: Aligned DataFrames.
  """
  # Convert dfs to DataFrame if it's a Series
  if isinstance(df1, pd.Series):
    df1 = pd.DataFrame(df1, columns=[df1.name])
  if isinstance(df2, pd.Series):
    df2 = pd.DataFrame(df2, columns=[df2.name])

  # Ensure the DataFrames have the same index
  df1 = df1[df1.index.isin(df2.index)]
  df2 = df2[df2.index.isin(df1.index)]

  # Combine the DataFrames to handle NaN removal efficiently
  combined_df = pd.concat([df1, df2], axis=1)

  # Drop rows with NaN values
  combined_df = combined_df.dropna()

  # Split the DataFrames back
  df1_aligned = combined_df[df1.columns]
  df2_aligned = combined_df[df2.columns]

  print(
      "DataFrames aligned based on length and index. Rows with NaN values removed."
  )

  return df1_aligned, df2_aligned


# Function to calculate Beta
def calculate_betas(stock_returns, market_returns):
  """
  Calculate financial betas for each stock given the daily returns of multiple stocks and the daily returns of the overall market.
  
  Parameters:
  - stock_returns (pd.DataFrame): DataFrame with daily returns of multiple stocks.
  - market_returns (pd.Series): Series with daily returns of the overall market.
  
  Returns:
  - pd.Series: Series containing financial betas for each stock.
  """

  # Ensure the input DataFrames have the same length, if not trimming them till they have the same length
  if len(stock_returns) != len(market_returns):
    stock_returns, market_returns = align_dataframes(stock_returns,
                                                     market_returns)

  # Initialize an empty Series to store betas
  betas = pd.Series(index=stock_returns.columns, dtype=float)

  # Iterate over each stock
  for stock in stock_returns.columns:
    # Extract stock and market returns as 1-dimensional arrays
    stock_returns_array = stock_returns[stock].values.reshape(-1, 1)
    market_returns_array = market_returns.values.reshape(-1, 1)

    # Combine stock and market returns into a DataFrame
    data = pd.DataFrame({
        'Stock': stock_returns_array.flatten(),
        'Market': market_returns_array.flatten()
    })

    # Drop rows with NaN values
    data = data.dropna()

    # Extract X (market returns) and y (stock returns)
    X = data[['Market']]
    y = data['Stock']

    # Fit a linear regression model
    model = LinearRegression().fit(X, y)

    # Retrieve the beta coefficient
    beta = model.coef_[0]

    # Store the beta in the betas Series
    betas[stock] = beta

  return betas


# Function to build Scatter Plot of Market and 1 selected Stock
def beta_scatterplot(stock_returns, market_returns, selected_stock):
  """
  Create a scatter plot for a specific stock against market returns.

  Parameters:
  - stock_returns (pd.DataFrame): DataFrame with daily returns of multiple stocks.
  - market_returns (pd.Series): Series with daily returns of the overall market.
  - selected_stock (str): The specific stock for which to create the scatter plot.
  
  Returns:
  - plt: The created plot.
  """

  # Ensure the input DataFrames have the same length, if not trimming them till they have the same length
  if len(stock_returns) != len(market_returns):
    stock_returns, market_returns = align_dataframes(stock_returns,
                                                     market_returns)

  # Create a DataFrame for the selected stock
  selected_data = pd.DataFrame({
      'Market':
      market_returns.values.flatten(),  # Convert to 1-dimensional array
      'Stock':
      stock_returns[selected_stock].values.flatten(
      )  # Convert to 1-dimensional array
  })

  # Set up the figure and axes
  plt.figure(figsize=(10, 6))
  plt.title(f'Scatter Plot for {selected_stock} Returns vs. Market Return')

  # Create a scatter plot with regression line using Seaborn
  sns.regplot(x='Market',
              y='Stock',
              data=selected_data,
              scatter=True,
              truncate=False,
              line_kws={
                  'linestyle': '--',
                  'color': 'red'
              },
              scatter_kws={'color': 'black'})

  # Set axis labels
  plt.xlabel('Market Returns (in percent)')
  plt.ylabel(f'{selected_stock} Returns (in percent)')

  # Add lines for x and y axes
  plt.axhline(0, color='black', linewidth=0.5)
  plt.axvline(0, color='black', linewidth=0.5)

  # Set padding so that all data points can be seen
  x_padding = 0.005
  y_padding = 0.005
  x_min = selected_data['Market'].min() - x_padding
  x_max = selected_data['Market'].max() + x_padding
  y_min = selected_data['Stock'].min() - y_padding
  y_max = selected_data['Stock'].max() + y_padding

  # Center the plot around (0,0)
  plt.xlim(min(x_min, -x_max), max(x_max, -x_min))
  plt.ylim(min(y_min, -y_max), max(y_max, -y_min))

  # Return the plot
  return plt


def save_all_scatterplots(stock_returns, market_returns):
  """
  If user wants, save all scatterplots to a user-defined place.

  Parameters:
  - stock_returns (pd.DataFrame): DataFrame with daily returns of multiple stocks.
  - market_returns (pd.Series): Series with daily returns of the overall market.
  """

  # Showcase an example of the graph
  beta_scatterplot(stock_returns, market_returns,
                   stock_returns.columns.values[0]).show()

  while True:
    # Get user input if they want to save the charts
    save_plots = input(
        "This is an example of the scattergraphs you can save.\nDo you want to save all scaterplots as such images?\nPlease answer 'yes' or 'no': "
    ).upper()

    if save_plots == 'YES':
      while True:
      # Get the file path from the user
          file_path = input("\nEnter only the file path of the destination folder")
          if os.path.exists(file_path):   
              try:
            # Save each plot and add the ticker to the name of the file
                  for stock in list(stock_returns.columns.values):
                      plot = beta_scatterplot(stock_returns, market_returns, stock)
                      entire_file_path = file_path + "\\" + stock + "-scatterplot.png"
                      plot.savefig(entire_file_path)
                      print(f"Scatterplot for {stock} saved to {entire_file_path}")
                  print(
                    "\nThank you for using this program. I hope this program was useful for you. Feel free to run it again"
                  )
                  break  # Exit the loop if the user successfully saves the plot
          # Use Error Handling if the user enters an invalid path
              except (FileNotFoundError, PermissionError) as e:
                  print(f"\nError: {e}. Please enter a valid file path.")
          else:
              print(f"\nThe path '{file_path}' does not lead to a folder. Please ensure that you do not reference another file")
      break
    elif save_plots == 'NO':
      print(
          "\nThank you for your input. I hope this program was useful for you. Feel free to run it again"
      )
      break
    else:
      print(
          "\nWarning: Invalid input. Please enter valid response ('yes' or 'no')"
      )


# End of all functions

# Main script:
def main():
  # Predefined list of allowed stock tickers
  allowed_tickers = [
      'MSFT', 'AAPL', 'AMZN', 'NVDA', 'GOOGL', 'META', 'GOOG', 'TSLA', 'UNH',
      'LLY', 'JPM', 'XOM', 'V', 'AVGO', 'JNJ', 'PG', 'MA', 'HD', 'ADBE', 'MRK',
      'CVX', 'COST', 'ABBV', 'WMT', 'PEP', 'KO', 'CSCO', 'CRM', 'ACN', 'MCD',
      'NFLX', 'LIN', 'BAC', 'AMD', 'ORCL', 'TMO', 'CMCSA', 'PFE', 'DIS', 'ABT',
      'INTC', 'VZ', 'WFC', 'INTU', 'AMGN', 'PM', 'COP', 'QCOM', 'IBM', 'NKE',
      'TXN', 'DHR', 'UNP', 'NOW', 'SPGI', 'GE', 'HON', 'AMAT', 'RTX', 'CAT',
      'SBUX', 'T', 'LOW', 'NEE', 'BA', 'BKNG', 'ELV', 'GS', 'BMY', 'TJX', 'DE',
      'UPS', 'LMT', 'MMC', 'ISRG', 'PLD', 'VRTX', 'MS', 'PGR', 'MDLZ', 'GILD',
      'ADP', 'MDT', 'SYK', 'BLK', 'CB', 'AXP', 'ETN', 'LRCX', 'CVS', 'CI',
      'REGN', 'AMT', 'ADI', 'SCHW', 'MU', 'C', 'ZTS', 'CME', 'SNPS', 'TMUS',
      'BSX', 'SLB', 'PANW', 'SO', 'FI', 'MO', 'EQIX', 'EOG', 'CDNS', 'KLAC',
      'BX', 'DUK', 'BDX', 'AON', 'NOC', 'ITW', 'WM', 'MCK', 'ICE', 'CL', 'HUM',
      'CSX', 'SHW', 'PYPL', 'ORLY', 'APD', 'CMG', 'MPC', 'FDX', 'GD', 'ROP',
      'PXD', 'TDG', 'MCO', 'ANET', 'AJG', 'PH', 'USB', 'MSI', 'MMM', 'APH', 'TT',
      'PSX', 'ABNB', 'TGT', 'EMR', 'MAR', 'AZO', 'FCX', 'PNC', 'LULU', 'WELL',
      'NXPI', 'HCA', 'CTAS', 'PCAR', 'AIG', 'ECL', 'NSC', 'SRE', 'ADSK', 'AFL',
      'VLO', 'WMB', 'CARR', 'ROST', 'CCI', 'HLT', 'CHTR', 'MNST', 'KMB', 'OXY',
      'MCHP', 'MSCI'
  ]
  
  print("Welcome to this Financial Beta calculator and visualiser\n")
  # Set the basic data (Dates, Tickers and Market_Proxy)
  stocks = get_stock_tickers(allowed_tickers)
  print("\nSelected stock tickers: ", stocks)
  market_proxy = '^GSPC'
  print(f"The market proxy is stock ticker: '{market_proxy}'")
  start_date = user_input_find_weekday()
  end_date = datetime.today().strftime('%Y-%m-%d')
  
  # Retrieve the daily returns for the selected stocks and the market
  adj_close__stocks_df = import_adj_close_data(stocks, start_date, end_date)
  adj_close__mkt_df = import_adj_close_data(market_proxy, start_date, end_date)
  
  # Calculate the daily returns for the selected stocks and the Market
  returns_stock_df = calc_daily_returns(adj_close__stocks_df)
  returns_mkt_df = calc_daily_returns(adj_close__mkt_df)
  
  # Calculate and show the Betas
  betas_df = calculate_betas(returns_stock_df, returns_mkt_df)
  print(f"\nThe table below shows the betas using daily returns over the following timeframe: {start_date} until {end_date}")
  print(betas_df)
  
  save_all_scatterplots(returns_stock_df, returns_mkt_df)


  

if __name__ == "__main__":
  main()