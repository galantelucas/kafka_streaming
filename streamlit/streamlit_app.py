import psycopg2
import pandas as pd
import streamlit as st
import time

# Função para buscar dados do banco de dados
def fetch_data():
    conn = psycopg2.connect(
        host="db",
        database="sales_db",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    cur.execute('SELECT sale_id, product, amount FROM sales')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return pd.DataFrame(rows, columns=['sale_id', 'product', 'amount'])

st.title('Dados de Vendas')

# Exibindo dados periodicamente
while True:
    df = fetch_data()
    st.dataframe(df)
    time.sleep(5)  # Atualiza a cada 5 segundos
    st.rerun()
