import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

st.title("Fraud Detection Dashboard")

conn = psycopg2.connect(
    dbname="fraud",
    user="user",
    password="password",
    host="postgres",
    port="5432"
)

@st.cache_data
def load_data():
    query = "SELECT * FROM scores ORDER BY id DESC LIMIT 100"
    return pd.read_sql(query, conn)

data = load_data()

st.subheader("Последние 10 транзакций с fraud_flag=1")
frauds = data[data["fraud_flag"] == True].head(10)
st.dataframe(frauds)

st.subheader("Распределение скорингов")
fig, ax = plt.subplots()
ax.hist(data["score"], bins=20, color="skyblue", edgecolor="black")
st.pyplot(fig)
