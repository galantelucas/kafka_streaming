import psycopg2
import time
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from decimal import Decimal
import plotly.express as px

# Configurações da Página
st.set_page_config(
    page_title="Unifor - Streaming",
    page_icon=":bar_chart:",
    layout="wide"
)

# Função para buscar dados do banco de dados, com cache de 5 segundos
@st.cache_data(ttl=5)
def fetch_data():
    conn = psycopg2.connect(
        host="db",
        database="sales_db",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    cur.execute('SELECT sale_id, product, amount, latitude, longitude, sale_date FROM sales')
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Converte os dados em DataFrame e ajusta os tipos de dados
    df = pd.DataFrame(rows, columns=['sale_id', 'product', 'amount', 'latitude', 'longitude', 'sale_date'])
    df['amount'] = df['amount'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
    df['latitude'] = df['latitude'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
    df['longitude'] = df['longitude'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
    df['sale_date'] = pd.to_datetime(df['sale_date'])

    return df
while True:
    df = fetch_data()

    # Menu de navegação
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Vendas", "Visualização Georreferenciada"],
            icons=["currency-dollar", "geo-alt-fill"]
        )

    # Exibe os dados com base na seleção do menu
    if selected == "Visualização Georreferenciada":
        st.title('Projeto de Processamento em Streaming')
        st.subheader('Unifor - Especialização em Engenharia de Dados')
        st.text("Alunos: Lucas Galante e Wilkerson Carvalho")
        st.markdown("---")
        st.subheader(":globe_with_meridians: Mapa de Vendas por Localização")
        st.map(df[['latitude', 'longitude']])
        st.write("")

    elif selected == "Vendas":
        # Título do dashboard
        st.title('Projeto de Processamento em Streaming')
        st.subheader('Unifor - Especialização em Engenharia de Dados')
        st.text("Alunos: Lucas Galante e Wilkerson Carvalho")
        st.markdown("---")
        st.subheader(":bar_chart: Dashboard Comercial")

        # Calcula total de vendas e número de transações
        total_amount = df['amount'].sum()
        total_sales = df['sale_id'].count()
        num_transactions = len(df)

        st.markdown("### Resumo de Vendas")
        last_refresh = st.empty()
        utc_time = datetime.now()  # Pegar o horário UTC
        brasil_time = utc_time - timedelta(hours=3)  # Ajustar para o fuso horário de Brasília (UTC-3)
        last_refresh.text(f"Última atualização em: {brasil_time.strftime('%Y-%m-%d %H:%M:%S')}")
        st.write("")

        # Dicionário de cores para que os produtos tenham sempre a mesma cor
        color_map = {
            'Product A': '#05668d',
            'Product B': '#c4b7cb',
            'Product C': '#f0f3bd'
        }

        # Ajustando cards de indicadores em 2 colunas com total de vendas e total de transações
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"""
                <div style="background-color:#021035;padding:20px;border-radius:10px;text-align:center;margin-bottom:20px;">
                    <h3 style="color:#4baab4">Total de Vendas</h3>
                    <p style="font-size:24px;color:white">${total_amount:,.2f}</p>
                </div>
                """, unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div style="background-color:#021035;padding:20px;border-radius:10px;text-align:center;margin-bottom:20px;">
                    <h3 style="color:#4baab4">Número de Transações</h3>
                    <p style="font-size:24px;color:white">{num_transactions}</p>
                </div>
                """, unsafe_allow_html=True
            )

        # Adiciona espaçamento após os cards de métricas
        st.write("")
        st.markdown("### Distribuição por Produto")
        st.write("")

        # Organizando duas colunas para os gráficos de rosca
        col3, col4 = st.columns(2)

        # Agrupa por produto e calcula o percentual de venda por valor e por quantidade
        product_amount = df.groupby('product')['amount'].sum().reset_index()
        product_amount['percent'] = (product_amount['amount'] / total_amount) * 100

        product_sales = df.groupby('product')['sale_id'].count().reset_index()
        product_sales['percent'] = (product_sales['sale_id'] / total_sales) * 100

        # Ordenando os DataFrames pelo valor e número de vendas
        product_amount = product_amount.sort_values(by='amount', ascending=False)
        product_sales = product_sales.sort_values(by='sale_id', ascending=False)

        # Gráfico de rosca com Plotly
        with col3:
            fig = px.pie(
                product_amount, values='amount', names='product',
                hole=0.4, title="Distribuição por Valor", color='product',
                color_discrete_map=color_map
            )
            st.plotly_chart(fig)
            st.write("")

        with col4:
            fig = px.pie(
                product_sales, values='sale_id', names='product',
                hole=0.4, title="Distribuição por Quantidade", color='product',
                color_discrete_map=color_map
            )
            st.plotly_chart(fig)
            st.write("")

        col5, col6 = st.columns(2)
        # Gráfico de barras horizontais para valor
        with col5:
            fig_amount = px.bar(
                product_amount, x='amount', y='product',
                title="Distribuição por Valor",
                color='product',
                color_discrete_map=color_map
            )
            st.plotly_chart(fig_amount)
            st.write("")

        # Gráfico de barras horizontais para quantidade
        with col6:
            fig_sales = px.bar(
                product_sales, x='sale_id', y='product',
                title="Distribuição por Quantidade",
                color='product',
                color_discrete_map=color_map
            )
            st.plotly_chart(fig_sales)
            st.write("")

        # Agrupa as vendas por mês e soma os valores
        sales_over_time = df.groupby([pd.Grouper(key='sale_date', freq='ME'), 'product'])['sale_id'].count().reset_index()

        # Criar o gráfico de linha para produtos vendidos por mês
        line_fig = px.line(
            sales_over_time, x='sale_date', y='sale_id', color='product',
            title='Produtos Vendidos por Mês', color_discrete_map=color_map
        )
        line_fig.update_layout(
            width=1200,  # Aumenta a largura
            height=500  # Aumenta a altura
        )

        line_fig.update_xaxes(title_text='Mês/Ano')
        line_fig.update_yaxes(title_text='Total de Vendas')
        line_fig.update_xaxes(dtick="M1", tickformat="%b\n%Y")  # Formato para mostrar mês e ano
        st.plotly_chart(line_fig)

        # Tabela de vendas
        st.markdown("#### Tabela de Vendas por Produto")
        st.table(df)
        st.write("")

    time.sleep(5)
    st.rerun()