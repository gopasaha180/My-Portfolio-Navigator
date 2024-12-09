# import all necessary libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
import numpy as np

#st.set_page_config(layout="wide")

st.title("📊Optimizes my Portfolio in Real-Time 📈")

st.image("stock-market.jpg", width=700)
st.markdown('---')
st.header("Context")
st.write("Stocks and financial instrument trading is a lucrative proposition. Stock markets across the world facilitate such trades and thus wealth exchanges hands. Stock prices move up and down all the time and having ability to predict its movement has immense potential to make one rich.")
st.header("Relation to the Context")
st.write("I am a stock investor. My investment approach is rooted in data analysis, pattern recognition, and machine learning, allowing me to identify trends and opportunities in the stock market with precision and efficiency.")
st.header("Purpose")
st.write("The purpose of creating Python Dashboard that Optimizes my Portfolio in Real-Time is to provide a dynamic, data-driven platform that allow me to monitor and adjust my investment portfolios efficiently.")
