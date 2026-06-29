import streamlit as st
from google.cloud import bigquery
import pandas as pd

def get_bigquery_client():
    credentials_info = st.secrets["gcp_service_account"]
    return bigquery.Client.from_service_account_info(credentials_info)

@st.cache_data(ttl=600)
def query_media_gols():
    client = get_bigquery_client()
    query = "SELECT media_gols_brasil FROM `projeto-copa-500721.copa.vw_media-gols-brasil` LIMIT 1"
    df = client.query(query).to_dataframe()
    return df["media_gols_brasil"].iloc[0] if not df.empty else 0.0

@st.cache_data(ttl=600)
def query_porcentagem_nao_perdido():
    client = get_bigquery_client()
    query = "SELECT porcentagem_nao_perdido FROM `projeto-copa-500721.copa.vw_porcentagem-vitorias-empates-brasil` LIMIT 1"
    return df["porcentagem_nao_perdido"].iloc[0] if not df.empty else 0.0

@st.cache_data(ttl=600)
def query_partidas_disputadas():
    client = get_bigquery_client()
    query = "SELECT numero_partidas FROM `projeto-copa-500721.copa.partidas-disputadas-brasil` LIMIT 1"
    df = client.query(query).to_dataframe()
    return df["numero_partidas"].iloc[0] if not df.empty else 0

media_gols_valor = query_media_gols()
porcentagem_nao_perdido_valor = query_porcentagem_nao_perdido()
partidas_disputadas_valor = query_partidas_disputadas()

media_gols_formatado = f"{media_gols_valor:.2f}"
porcentagem_nao_perdido_formatado = f"{porcentagem_nao_perdido_valor}%"
partidas_disputadas_formatado = f"{partidas_disputadas_valor}"

# Interface

st.header("Indicadores") 

col1, col2, col3 = st.columns(3)

with col1: 
    st.metric(label="Média de gols", value=media_gols_formatado) 
with col2: 
    st.metric(label="% de jogos sem derrotas", value=porcentagem_nao_perdido_formatado) 
with col3: 
    st.metric(label="Partidas disputadas", value=partidas_disputadas_formatado)
