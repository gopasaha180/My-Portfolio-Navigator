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


data = yf.download(ticker_symbol, start=start_date, end=end_date, group_by='ticker_symbol')

if data.empty:
    st.warning("⚠️ No data returned. Try changing the stock ticker or date range.")
else:
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

    if data.empty:
        st.error("No pricing data available to analyze. Please check the stock ticker or date range.")
    elif 'Adj Close' not in data.columns:
        st.error("The 'Adj Close' column is missing from the dataset.")
    else:
        st.write("I have added a new column **%Change** and calculated **Annual Return**, **Standard Deviation**, **Risk Adj. Return** here.")
        st.write("**%Change:** Daily percentage change from previous Adj Close.")
        
        data2 = data.copy()
        data2['% Change'] = data2['Adj Close'] / data2['Adj Close'].shift(1) - 1
        st.write(data2)

        annual_return = data2['% Change'].mean() * 252 * 100    
        st.write(f'Annual Return: {annual_return:.2f}%')

        stdev = np.std(data2['% Change']) * np.sqrt(252)
        st.write(f'Standard Deviation: {stdev * 100:.2f}%')

        risk_adj_return = annual_return / (stdev * 100)
        st.write(f'Risk Adj. Return: {risk_adj_return:.2f}')


with chart:
    st.subheader('Chart')
    st.write("**Overall Impression:** The graph appears to depict the historical price fluctuations of a particular asset over a period. The **Adj Close** on the y-axis likely represents the adjusted closing price of the asset on each trading day. The graph exhibits significant volatility. The price line fluctuates considerably, suggesting that the asset's value has experienced periods of both substantial gains and losses.")
    fig = px.line(data, x = data.index, y=data['Adj Close'], title=ticker_symbol)
    st.plotly_chart(fig)    

st.write("**Notice** also that weekends are missing from the records.")
st.write("**Disclaimer:** Stock prices are subject to change at any time and involve inherent risks. This information is for general knowledge and informational purposes only and does not constitute financial advice.")
