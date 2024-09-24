import psycopg2
import pandas as pd
import streamlit as st
from decimal import Decimal
import plotly.express as px

# Função para buscar dados do banco de dados, com cache de 5 segundos para atualizar periodicamente
@st.cache_data(ttl=5)  # Atualiza os dados a cada 5 segundos
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
    df['sale_date'] = pd.to_datetime(df['sale_date'], format='%Y%m%d')
    
    return df

# Título do dashboard
st.title('Dashboard de Vendas')

# Menu de navegação
menu = st.sidebar.selectbox("Menu", ["Detalhamento de Produtos e Vendas", "Visualização Georreferenciada"])

# Exibe os dados com base na seleção do menu
df = fetch_data()  # Carrega os dados com cache e atualização automática

if menu == "Visualização Georreferenciada":
    st.markdown("### Mapa de Vendas por Localização")
    st.map(df[['latitude', 'longitude']])
    st.write("")  

elif menu == "Detalhamento de Produtos e Vendas":
    # Calcula total de vendas e número de transações
    total_sales = df['amount'].sum()
    num_transactions = len(df)
    
    # Layout das métricas com cards customizados
    st.markdown("### Resumo de Vendas")
    st.write("") 

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div style="background-color:#021035;padding:20px;border-radius:10px;text-align:center;margin-bottom:20px;">
                <h3 style="color:#4baab4">Total de Vendas</h3>
                <p style="font-size:24px;color:white">${total_sales:,.2f}</p>
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
    st.markdown("### Detalhes das Vendas e Distribuição por Produto")
    st.write("") 

    # Agrupa por produto e calcula o percentual de cada um
    product_sales = df.groupby('product')['amount'].sum().reset_index()
    product_sales['percent'] = (product_sales['amount'] / total_sales) * 100
    
    # Organizando a tabela e o gráfico em duas colunas
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### Tabela de Vendas por Produto")
        st.dataframe(df)

    with col4:
        st.markdown("#### Distribuição de Vendas por Produto")
        # Gráfico de rosca com Plotly
        fig = px.pie(product_sales, values='amount', names='product', hole=0.4, title="Distribuição de Vendas")
        st.plotly_chart(fig)

    # Agrupa as vendas por mês e soma os valores
    sales_over_time = df.groupby(pd.Grouper(key='sale_date', freq='M'))['amount'].sum().reset_index()

    # Criando o gráfico de linha
    line_fig = px.line(sales_over_time, x='sale_date', y='amount', title='Vendas ao Longo do Tempo')
    line_fig.update_xaxes(title_text='Data')
    line_fig.update_yaxes(title_text='Total de Vendas')
    line_fig.update_xaxes(dtick="M1", tickformat="%b\n%Y")  # Formato para mostrar mês e ano
    st.plotly_chart(line_fig)
   
    st.write("")
