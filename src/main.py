import streamlit as st
from google.cloud import bigquery
import pandas as pd
import plotly.express as px

def get_bigquery_client():
    credentials_info = st.secrets["gcp_service_account"]
    return bigquery.Client.from_service_account_info(credentials_info)

# Queries para o Google Cloud

@st.cache_data(ttl=600)
def query_media_gols():
    client = get_bigquery_client()
    query = "SELECT media_gols_brasil FROM `projeto-copa-500721.copa.vw_media-gols-brasil` LIMIT 1"
    df = client.query(query).to_dataframe()
    if df.empty:
        return 0.0
    return df[df.columns[0]].iloc[0]

@st.cache_data(ttl=600)
def query_porcentagem_nao_perdido():
    client = get_bigquery_client()
    query = "SELECT porcentagem_nao_perdido FROM `projeto-copa-500721.copa.vw_porcentagem-vitorias-empates-brasil` LIMIT 1"
    df = client.query(query).to_dataframe()
    if df.empty:
        return 0.0
    return df[df.columns[0]].iloc[0]

@st.cache_data(ttl=600)
def query_partidas_disputadas():
    client = get_bigquery_client()
    query = "SELECT numero_partidas FROM `projeto-copa-500721.copa.partidas-disputadas-brasil` LIMIT 1"
    df = client.query(query).to_dataframe()
    if df.empty:
        return 0
    return df[df.columns[0]].iloc[0]

@st.cache_data(ttl=600)
def query_gols_por_time():
    client = get_bigquery_client()
    # Uma query de exemplo que traz o ano e a quantidade de gols
    query = """
        SELECT *
        FROM `projeto-copa-500721.copa.vw_gols-por-time`
        LIMIT 10
    """
    df = client.query(query).to_dataframe()
    return df

media_gols_valor = query_media_gols()
porcentagem_nao_perdido_valor = query_porcentagem_nao_perdido()
partidas_disputadas_valor = query_partidas_disputadas()

gols_por_time_grafico = query_gols_por_time()

media_gols_formatado = f"{media_gols_valor:.2f}"
porcentagem_nao_perdido_formatado = f"{porcentagem_nao_perdido_valor}%" 
partidas_disputadas_formatado = f"{partidas_disputadas_valor}"

# Interface

st.header("Indicadores do Brasil") 

col1, col2, col3 = st.columns(3)

with col1: 
    st.metric(label="Média de gols", value=media_gols_formatado) 
with col2: 
    st.metric(label="% de jogos sem derrotas", value=porcentagem_nao_perdido_formatado) 
with col3: 
    st.metric(label="Partidas disputadas", value=partidas_disputadas_formatado)


fig = px.bar(
    gols_por_time_grafico, 
    x="player_team_name", 
    y="gols", 
    title="Gols por time",
    labels={
        "player_team_name": "Time",
        "gols": "Gols"
    },
    text_auto=True)
fig.update_traces(marker_color='green')
st.plotly_chart(fig, use_container_width=True)