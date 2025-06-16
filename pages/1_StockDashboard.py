# import all necessary libraries
import datetime
import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import altair as alt
import numpy as np

#st.set_page_config(layout="wide")

st.title('Yahoo Finance Data Viewer')
st.write("The Nasdaq Composite is a major stock market index that tracks the performance of most of the stocks listed on the Nasdaq Stock Market. The Nasdaq is an American stock exchange, known for listing many of the world's largest and most influential technology and biotechnology companies.")
st.write("Overall, this table provides a snapshot of the daily stock price movements for **Nasdaq Stock Market**.")

# Sidebar layout
st.sidebar.title('Please provide the following')

ticker_data = pd.read_csv("./data/nasdaq-listed.csv")
tickers = ticker_data['Symbol'].unique()
ticker_symbol = st.sidebar.selectbox('Pick your Stock Ticker',tickers)

start_date = st.sidebar.date_input('Start Date', value=datetime.date(2020, 1, 1))
end_date = st.sidebar.date_input('End Date', value=datetime.date.today())

st.subheader(f'{ticker_symbol} Stock Overview')
historical_data, pricing_data, chart = st.tabs(["Historical Data", "Pricing Data", "Chart"])

ticker = yf.Ticker(ticker_symbol)


# if start_date is not None and end_date is not None
data = yf.download(ticker_symbol, start=start_date, end=end_date, group_by='ticker_symbol')
data = data.stack(level=0).rename_axis(['Date', 'Ticker']).reset_index(level=1)



with historical_data:
    st.header('Historical Data')
    st.subheader('Column Descriptions')
    st.write('**Date:** This column represents the date for which the stock data is recorded. In this case, it is formatted as "YYYY-MM-DD 00:00:00"')
    st.write("**Ticker:** This column identifies the stock symbol.")
    st.write('**Open:** This column shows the opening price of the stock on that particular trading day.')
    st.write('**High:** This column indicates the highest price reached by the stock during that trading day.')
    st.write('**Low:** This column shows the lowest price reached by the stock during that trading day.')
    st.write('**Close:** This column represents the closing price of the stock at the end of the trading day.')
    st.write("**Adj Close:** This column shows the adjusted closing price. This value accounts for corporate actions like stock splits and dividends, providing a more accurate historical comparison of the stock's performance.")
    st.write('**Volume:** This column indicates the trading volume for that day, which represents the total number of shares traded.')
    st.write(data)

with pricing_data:
    st.subheader('Price Movements')
    st.write("I have added a new column **%Change** and calculated **Annual Return**, **Standard Devision**, **Risk Adj. Return** here. ")
    st.write("**%Change:** This column shows the percentage change in the stock's price from the previous day's Adj closing price.")
    st.write("**Annual Return:** The annual return represents the percentage change in the investment value over a year. It's a measure of the overall performance of an investment.")
    st.write("**Standard Deviation:** Standard deviation measures the volatility or risk associated with an investment. It quantifies how much the stock price fluctuates around its average price. A high standard deviation indicates that the stock price has experienced significant fluctuations, implying higher risk.")
    st.write("**Risk-Adjusted Return:** This metric attempts to measure the investment's return relative to its risk. It aims to determine whether the return generated is sufficient to compensate for the level of risk taken. A higher value generally indicates a better risk-adjusted performance. However, the interpretation of this value depends on the specific risk-adjusted return metric used.")
    data2 = data
    data2['% Change'] = data['Adj Close']/data['Adj Close'].shift(1) - 1
    st.write(data2)
    annual_return = data2['% Change'].mean()*252*100    
    st.write(f'Annual Return: {annual_return:.2f}%')
    stdev = np.std(data2['% Change'])*np.sqrt(252)    
    st.write(f'Standard Devision: {stdev*100:.2f}%')    
    st.write(f'Risk Adj. Return: {annual_return/(stdev*100):.2f}%')


with chart:
    st.subheader('Chart')
    st.write("**Overall Impression:** The graph appears to depict the historical price fluctuations of a particular asset over a period. The **Adj Close** on the y-axis likely represents the adjusted closing price of the asset on each trading day. The graph exhibits significant volatility. The price line fluctuates considerably, suggesting that the asset's value has experienced periods of both substantial gains and losses.")
    fig = px.line(data, x = data.index, y=data['Adj Close'], title=ticker_symbol)
    st.plotly_chart(fig)    

st.write("**Notice** also that weekends are missing from the records.")
st.write("**Disclaimer:** Stock prices are subject to change at any time and involve inherent risks. This information is for general knowledge and informational purposes only and does not constitute financial advice.")
