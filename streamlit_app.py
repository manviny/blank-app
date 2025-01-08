import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt

class SupportResistance:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def download_data(self):
        data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        return data

    def calculate_support_resistance(self, df):
        return df['Low'].min(), df['High'].max()

    def calculate_pivot_points(self, df):
        high = df['High'].max()
        low = df['Low'].min()
        close = df['Close'].iloc[-1]
        pivot = (high + low + close) / 3
        support1 = (2 * pivot) - high
        resistance1 = (2 * pivot) - low
        return pivot, support1, resistance1

    def plot_data(self, df):
        df['Close'].plot(title=f"{self.ticker} Closing Prices")
        support, resistance = self.calculate_support_resistance(df)
        pivot, support1, resistance1 = self.calculate_pivot_points(df)
        #plt.figure(figsize=(18, 16))
        plt.scatter(df.index, [support]*len(df), color='green', label='Support')
        plt.scatter(df.index, [resistance]*len(df), color='red', label='Resistance')
        plt.scatter(df.index, [pivot]*len(df), color='yellow', label='Pivot')
        plt.scatter(df.index, [support1]*len(df), color='orange', label='Support 1')
        plt.scatter(df.index, [resistance1]*len(df), color='purple', label='Resistance 1')
        plt.legend()
        plt.grid(True)
        
        st.pyplot(plt)

# Streamlit app layout
st.title("Financial Data Viewer")

# Layout for inputs using columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    # User input for ticker selection
    ticker = st.text_input("Enter ticker", "AAPL")

with col2:
    # User input for date range
    start_date = st.date_input("Start date", datetime.date.today() - datetime.timedelta(days=365))

with col3:
    end_date = st.date_input("End date", datetime.date.today())

with col4:
    # Button to show the chart
    show_chart = st.button("Show Chart")

if show_chart:
    sr = SupportResistance(ticker, start_date, end_date)
    df = sr.download_data()
    if not df.empty:
        sr.plot_data(df)
    else:
        st.write("No data available for the selected ticker.")
