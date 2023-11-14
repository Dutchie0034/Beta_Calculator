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
4. [Main Script](#main-script)
5. [Example Usage](#example-usage)
6. [Dependencies](#dependencies)

## Installation
Ensure that you have the required libraries installed. You can install them using: <br>
pip install pandas matplotlib seaborn yfinance scikit-learn


## Usage
To use the functions provided in this project, run the main() function in the script.

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

## Main Script
The main script initializes the project, gets user inputs which stocks in which time frame should be analysed, retrieves data from Yahoo Finance through an API at yfinance, calculates betas, visualizes 1 scatterplot and asks the user if and where they want to save all scatterplots.

## Example Usage
python financial_beta_calculator.py

## Dependencies
- [pandas](https://pandas.pydata.org/docs/)
- [matplotlib](https://matplotlib.org/stable/index.html)
- [seaborn](https://seaborn.pydata.org/)
- [yfinance](https://pypi.org/project/yfinance/)
- [scikit-learn](https://scikit-learn.org/stable/)
