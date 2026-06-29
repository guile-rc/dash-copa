import streamlit as st
from google.cloud import bigquery
import pandas as pd

def get_bigquery_client():
    credentials_info = st.secrets["gcp_service_account"]
    return bigquery.Client.from_service_account_info(credentials_info)

@st.cache_data(ttl=600)
def load_data_from_view():
    client = get_bigquery_client()
    
    query = """
        SELECT * FROM `seu-projeto-gcp.seu_dataset.sua_view` 
        LIMIT 100
    """
    
    query_job = client.query(query)
    df = query_job.to_dataframe()
    return df

# Interface

st.header("Indicadores") 

col1, col2, col3 = st.columns(3) 

with col1: st.metric(label="Média de gols", value="00") 
with col2: st.metric(label="% de jogos sem derrotas", value="00") 
with col3: st.metric(label="Partidas disputadas", value="00")
