#!/usr/bin/env python3
"""Dashboard Streamlit para as 5 perguntas do projeto.

Use: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from pathlib import Path


DB = Path("data.db")


@st.cache_data
def load_data():
    if not DB.exists():
        st.error("Banco de dados data.db não encontrado. Rode load_to_sqlite.py primeiro.")
        return pd.DataFrame()
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
    return df


def main():
    st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
    st.title("Dashboard - Gestão Financeira Global")

    df = load_data()
    if df.empty:
        return

    # Ajustes de tipos
    if 'Ano' not in df.columns and 'Data_Pedido' in df.columns:
        df['Ano'] = pd.to_datetime(df['Data_Pedido'], dayfirst=True, errors='coerce').dt.year

    # Filtros
    years = sorted(df['Ano'].dropna().unique().astype(int).tolist())
    segments = sorted(df['Segmento'].dropna().unique().tolist())
    countries = sorted(df['Pais'].dropna().unique().tolist())

    with st.sidebar:
        st.header('Filtros')
        year = st.selectbox('Ano', options=['Todos'] + years, index=0)
        segment = st.selectbox('Segmento', options=['Todos'] + segments, index=0)
        country = st.selectbox('País', options=['Todos'] + countries, index=0)

    # Aplicar filtros
    dff = df.copy()
    if year != 'Todos':
        dff = dff[dff['Ano'] == int(year)]
    if segment != 'Todos':
        dff = dff[dff['Segmento'] == segment]
    if country != 'Todos':
        dff = dff[dff['Pais'] == country]

    # Pergunta 1 - total vendido
    total_vendido = dff['Total_Vendas'].sum()
    st.metric('Total Vendido', f"{total_vendido:,.2f}")

    # Pergunta 2 - vendas por categoria
    st.subheader('Vendas por Categoria')
    cat = dff.groupby('Categoria').agg(qtd_vendas=('ID_Pedido', 'count'), valor_vendas=('Total_Vendas', 'sum')).reset_index()
    fig_cat = px.bar(cat.sort_values('qtd_vendas', ascending=False), x='Categoria', y='qtd_vendas', hover_data=['valor_vendas'], labels={'qtd_vendas':'Quantidade de Vendas'})
    st.plotly_chart(fig_cat, use_container_width=True)

    # Pergunta 3 - vendas por país considerando prioridade
    st.subheader('Vendas por País e Prioridade')
    pc = dff.groupby(['Pais', 'Prioridade']).size().reset_index(name='qtd_vendas')
    if not pc.empty:
        fig_pc = px.bar(pc, x='Pais', y='qtd_vendas', color='Prioridade', title='Vendas por País e Prioridade')
        st.plotly_chart(fig_pc, use_container_width=True)
    else:
        st.write('Nenhum dado para os filtros selecionados.')

    # Pergunta 4 - média de desconto por subcategoria
    st.subheader('Média de Desconto por Subcategoria')
    ds = dff.groupby('SubCategoria').agg(desconto_medio=('Desconto', 'mean')).reset_index()
    fig_ds = px.bar(ds.sort_values('desconto_medio', ascending=False), x='SubCategoria', y='desconto_medio')
    st.plotly_chart(fig_ds, use_container_width=True)

    # Pergunta 5 - países com maior média de valor de venda (mapa)
    st.subheader('Média de Valor de Venda por País (Mapa)')
    mp = dff.groupby('Pais').agg(valor_medio_venda=('Total_Vendas', 'mean')).reset_index()
    if not mp.empty:
        try:
            fig_map = px.choropleth(mp, locations='Pais', locationmode='country names', color='valor_medio_venda', title='Valor Médio de Venda por País')
            st.plotly_chart(fig_map, use_container_width=True)
        except Exception as e:
            st.write('Falha ao gerar mapa interativo:', e)
            st.dataframe(mp.head())
    else:
        st.write('Nenhum dado para o mapa com os filtros aplicados.')

    # Opção de download dos dados filtrados
    st.sidebar.markdown('---')
    st.sidebar.download_button('Baixar dados filtrados (CSV)', dff.to_csv(index=False), file_name='dados_filtrados.csv')


if __name__ == '__main__':
    main()
