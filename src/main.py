import streamlit as st
from google.cloud import bigquery
import pandas as pd
import plotly.express as px

def get_bigquery_client():
    credentials_info = st.secrets["gcp_service_account"]
    return bigquery.Client.from_service_account_info(credentials_info)

# QUERIES PARA O GOOGLE CLOUD
# ===========================
# Indicadores

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

media_gols_valor = query_media_gols()
porcentagem_nao_perdido_valor = query_porcentagem_nao_perdido()
partidas_disputadas_valor = query_partidas_disputadas()

media_gols_formatado = f"{media_gols_valor:.2f}"
porcentagem_nao_perdido_formatado = f"{porcentagem_nao_perdido_valor}%" 
partidas_disputadas_formatado = f"{partidas_disputadas_valor}"

# Gráficos

@st.cache_data(ttl=600)
def query_gols_por_time():
    client = get_bigquery_client()
    query = """
        SELECT *
        FROM `projeto-copa-500721.copa.vw_gols-por-time`
        LIMIT 10
    """
    df = client.query(query).to_dataframe()
    return df
gols_por_time_grafico = query_gols_por_time()

@st.cache_data(ttl=600)
def query_classificacoes():
    client = get_bigquery_client()
    query = """
        SELECT *
        FROM `projeto-copa-500721.copa.vw_times-classificados`
        LIMIT 10
    """
    df = client.query(query).to_dataframe()
    return df
classificacoes_grafico = query_classificacoes()

@st.cache_data(ttl=600)
def query_desempenho():
    client = get_bigquery_client()
    query = """
        SELECT year, count_matches
        FROM `projeto-copa-500721.copa.vw_desempenho-brasil`
    """
    df = client.query(query).to_dataframe()
    return df
desempenho_grafico = query_desempenho()

@st.cache_data(ttl=600)
def query_gols_por_jogador():
    client = get_bigquery_client()
    query = """
        SELECT *
        FROM `projeto-copa-500721.copa.vw_jogadores-por-gols`
    """
    df = client.query(query).to_dataframe()
    return df
gols_por_jogador_grafico = query_gols_por_jogador()

@st.cache_data(ttl=600)
def query_gols_e_partidas_por_jogador():
    client = get_bigquery_client()
    query = """
        SELECT *
        FROM `projeto-copa-500721.copa.vw_gols-e-partidas-por-jogador`
    """
    df = client.query(query).to_dataframe()
    return df
gols_e_partidas_por_jogador_grafico = query_gols_e_partidas_por_jogador()

# INTERFACE
# =========

st.header("Indicadores do Brasil") 

col_metric_1, col_metric_2, col_metric_3 = st.columns(3)

with col_metric_1: 
    st.metric(label="Média de gols", value=media_gols_formatado) 
with col_metric_2: 
    st.metric(label="% de jogos sem derrotas", value=porcentagem_nao_perdido_formatado) 
with col_metric_3: 
    st.metric(label="Partidas disputadas", value=partidas_disputadas_formatado)


col_plot_1, col_plot_2 = st.columns(2)

with col_plot_1:
    # Gols por time
    fig_gols = px.bar(
        gols_por_time_grafico, 
        x="player_team_name", 
        y="gols", 
        title="Gols por time",
        labels={
            "player_team_name": "Time",
            "gols": "Gols"
        },
        text_auto=True)
    fig_gols.update_traces(marker_color='green')
    st.plotly_chart(fig_gols, use_container_width=True)
with col_plot_2:
    # Quantidade de classificações por país
    fig_classificacoes = px.bar(
        classificacoes_grafico, 
        x="team_name", 
        y="classificacoes", 
        title="Quantidade de classificações por país",
        labels={
            "team_name": "Time",
            "classificacoes": "Classificações"
        },
        text_auto=True)
    fig_classificacoes.update_traces(marker_color='green')
    st.plotly_chart(fig_classificacoes, use_container_width=True)

# Desempenho
fig_desempenho = px.line(
    desempenho_grafico, 
    x="year", 
    y="count_matches",
    title="Desempenho do Brasil por Copa",
    labels={
        "year": "Copa",
        "count_matches": "Nº de partidas"
    })
fig_desempenho.update_traces(line_color='green')
fig_desempenho.update_xaxes(
    tickmode="linear",
    dtick=8,
    tick0=1930
)
st.plotly_chart(fig_desempenho, use_container_width=True)

# Gols por jogador
fig_gols_por_jogador = px.bar(
    gols_por_jogador_grafico, 
    x="nome", 
    y="gols", 
    title="Gols por jogador",
    labels={
        "nome": "Nome",
        "gols": "Gols"
    },
    text_auto=True)
fig_gols_por_jogador.update_traces(marker_color='green')
st.plotly_chart(fig_gols_por_jogador, use_container_width=True)

# Gols e partidas por jogador
fig_gols_e_partidas_por_jogador = px.scatter(
    gols_e_partidas_por_jogador_grafico, 
    x="partidas", 
    y="gols", 
    hover_name="nome",         
    title='Desempenho dos Jogadores do Brasil (Copas 2018 e 2022)',
    labels={
        "partidas": "Partidas",
        "gols": "Gols"
    },
    size="gols",                
    color="gols",               
    color_continuous_scale='Viridis'
)
fig_gols_por_jogador.update_layout(
    xaxis=dict(tickmode='linear', tick0=0, dtick=1),
    yaxis=dict(tickmode='linear', tick0=0, dtick=1)
)
st.plotly_chart(fig_gols_e_partidas_por_jogador, use_container_width=True)