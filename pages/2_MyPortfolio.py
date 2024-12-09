# import all necessary libraries
import datetime
import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import numpy as np

#st.set_page_config(layout="wide")

st.sidebar.title('Please provide the following')
start_date = st.sidebar.date_input('Start Date', value=datetime.date(2020, 1, 1))
end_date = st.sidebar.date_input('End Date', value="today")


tickers1 = ['NVDA','MSFT','GOOGL','META','IBM']
my_ticker_data = pd.read_csv("./data/mytickers.csv")
tickers = my_ticker_data['Symbol'].unique().tolist()
data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
returns = data.pct_change().dropna()


st.title("Protfolio Optimization Based on Number of Shares")

shares = {}
total_shares = 0

for ticker in tickers:
    num_shares = st.sidebar.number_input(f'Enter the number of shares for {ticker}', min_value=0, value=0)
    shares[ticker] = num_shares
    total_shares += num_shares

if total_shares > 0:
    weights = np.array([shares[ticker] / total_shares for ticker in tickers])
else:
    weights = np.zeros(len(tickers))

portfolio_returns = returns.dot(weights)
portfolio_cumulative_returns = (1 + portfolio_returns).cumprod()


portfolio_variance = np.dot(weights.T, np.dot(returns.cov() * 252, weights))
portfolio_volatility = np.sqrt(portfolio_variance)
expected_return = np.sum(returns.mean() * weights) * 252

st.write(f'**Annual Return:** {expected_return * 100:.2f}%')
st.write(f'**Volatility(Risk):** {portfolio_volatility * 100:.2f}%')


st.write("**Current Weight Based on Selected Shares (Static):**")
weight_dict_header = {"Ticker" : "% Weightage"}
weight_dict = {tickers[i]: weights[i]*100 for i in range(len(tickers))}
st.write(weight_dict_header|weight_dict)


st.line_chart(portfolio_cumulative_returns)

st.write("This interactive dashboard allows me to visualize and optimize the performance of a hypothetical portfolio based on the number of shares I hold in each of the selected stocks.")


st.write("**Calculation:** The dashboard dynamically calculates the portfolio's annual return, volatility (risk), and current weight based on the number of shares entered.")
st.write("**Visual Representation:** The interactive chart visualizes the portfolio's performance over time, providing insights into its growth and fluctuations.")
st.write("**Note:** Portfolio optimization also involves numerous factors, including risk tolerance, investment goals, and market conditions.")