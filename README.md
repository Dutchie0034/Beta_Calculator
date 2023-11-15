# Financial Beta Calculator and Visualizer

## Overview
This project provides a set of functions to calculate and visualize financial betas for selected stocks using daily returns and a market proxy. It includes functionalities for user input, data retrieval, beta calculation, and scatterplot visualization.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Functions](#functions)
    - [get_stock_tickers](#get_stock_tickers)
    - [user_input_find_weekday](#user_input_find_weekday)
    - [find_weekday_x_days_ago](#find_weekday_x_days_ago)
    - [import_adj_close_data](#import_adj_close_data)
    - [calc_daily_returns](#calc_daily_returns)
    - [align_dataframes](#align_dataframes)
    - [calculate_betas](#calculate_betas)
    - [beta_scatterplot](#beta_scatterplot)
    - [save_all_scatterplots](#save_all_scatterplots)
5. [Execution](#execution)
6. [Dependencies](#dependencies)

## Installation
Ensure that you have the required libraries installed. You can install them using: <br>
```python
pip install pandas matplotlib seaborn yfinance scikit-learn <br>
```

The program also uses the pre-installed os and datetime packages


## Usage
To use the functions provided in this project, run the main() function in the script. It executes the following steps
1. The program will ask you to choose at least 2 stock tickers (from a list of 175 tickers)
2. You choose how many weekdays into the past the analysis should take into account
3. The program will fetch every daily adj. close of your selected tickers and the S&P 500 (in a pandas dataframe) through the yfinance API from x weekdays ago until yesterday
4. The program will calculate the daily returns of all tickers and the S&P 500
5. The program will calculate the betas (using a linear regression from scikit-learn) and display them to you
6. The program will show you an example of a scatterplot (using seaborn and matplotlib) regressing a stock with the market over the defined time period
7. Please close it before the program will continue
8. You have the option to input a path to which the program saves .png images of the scatterplot of all your selected stocks
9. The program ends

## Functions

### get_stock_tickers
- Ask the user to input stock tickers to include in an analysis.
- Returns a list of valid stock tickers in string format.

### user_input_find_weekday
- Get user input for the number of weekdays they want to include in the analysis.
- Returns the date of the weekday x weekdays ago in 'YYYY-MM-DD' format.

### find_weekday_x_days_ago
- Find the date of the weekday that occurred x weekdays ago.
- Returns the date in 'YYYY-MM-DD' format.

### import_adj_close_data
- Import the data of the selected stock tickers and extract the adjusted closing date.
- Returns a DataFrame with the selected tickers and start and end dates.

### calc_daily_returns
- Calculate daily returns for each stock in the given DataFrame.
- Returns a DataFrame with daily returns for each stock in percent.

### align_dataframes
- Trim the top rows of the larger DataFrame (or Series) until they are of the same length.
- Remove rows with NaN values in either DataFrame.
- Returns aligned DataFrames.

### calculate_betas
- Calculate financial betas for each stock given the daily returns of multiple stocks and the daily returns of the overall market.
- Returns a Series containing financial betas for each stock.

### beta_scatterplot
- Create a scatter plot for a specific stock against market returns.
- Returns the created plot.

### save_all_scatterplots
- If the user wants, save all scatterplots to a user-defined place.


## Execution
Please download the financial_beta_calculator.py file, in your command line go to the folder where you saved the file and run the following script in your command line: <br>
```python
python financial_beta_calculator.py
```
## Dependencies
- [pandas](https://pandas.pydata.org/docs/)
- [matplotlib](https://matplotlib.org/stable/index.html)
- [seaborn](https://seaborn.pydata.org/)
- [yfinance](https://pypi.org/project/yfinance/)
- [scikit-learn](https://scikit-learn.org/stable/)
