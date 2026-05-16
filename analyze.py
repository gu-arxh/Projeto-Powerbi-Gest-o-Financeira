#!/usr/bin/env python3
"""Executa as queries em `analysis.sql` e gera gráficos.
Uso:
  python analyze.py --year 2014 --segment Consumidor --country "United States"
"""
import sqlite3
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path


DB = Path("data.db")
SQL = Path("analysis.sql")
OUT = Path("outputs")
OUT.mkdir(exist_ok=True)


def load_sql():
    txt = SQL.read_text()
    queries = {}
    cur_name = None
    cur_lines = []
    for line in txt.splitlines():
        if line.strip().startswith('-- name:'):
            if cur_name:
                queries[cur_name] = '\n'.join(cur_lines).strip()
            cur_name = line.split(':',1)[1].strip()
            cur_lines = []
        else:
            cur_lines.append(line)
    if cur_name:
        queries[cur_name] = '\n'.join(cur_lines).strip()
    return queries


def run_query(conn, sql, params):
    return pd.read_sql_query(sql, conn, params=params)


def save_bar(df, x, y, title, fname):
    plt.figure(figsize=(8,5))
    df_sorted = df.sort_values(y, ascending=False)
    plt.bar(df_sorted[x].astype(str), df_sorted[y])
    plt.xticks(rotation=45, ha='right')
    plt.title(title)
    plt.tight_layout()
    path = OUT / fname
    plt.savefig(path)
    plt.close()
    print(f"Gráfico salvo: {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int)
    parser.add_argument('--segment')
    parser.add_argument('--country')
    args = parser.parse_args()

    if not DB.exists():
        raise SystemExit("Banco de dados não encontrado. Rode `python load_to_sqlite.py` primeiro.")

    queries = load_sql()
    conn = sqlite3.connect(DB)

    params = {"year": args.year, "segment": args.segment, "country": args.country}

    # Pergunta 1
    df1 = run_query(conn, queries['total_sales'], params)
    total = df1['total_vendido'].iloc[0]
    print(f"Total vendido: {total}")

    # Pergunta 2
    df2 = run_query(conn, queries['sales_by_category'], params)
    save_bar(df2, 'categoria', 'qtd_vendas', 'Vendas por Categoria', 'vendas_por_categoria.png')
    df2.to_csv(OUT / 'vendas_por_categoria.csv', index=False)

    # Pergunta 3
    df3 = run_query(conn, queries['sales_by_country_priority'], params)
    df3.to_csv(OUT / 'vendas_por_pais_prioridade.csv', index=False)
    # Gerar pivot para visualização
    pivot = df3.pivot(index='pais', columns='prioridade', values='qtd_vendas').fillna(0)
    save_bar(pivot.reset_index().melt(id_vars='pais', var_name='prioridade', value_name='qtd_vendas').groupby('pais').sum().reset_index(), 'pais', 'qtd_vendas', 'Vendas por País (total)', 'vendas_por_pais_total.png')

    # Pergunta 4
    df4 = run_query(conn, queries['avg_discount_by_subcategory'], params)
    df4.to_csv(OUT / 'desconto_medio_subcategoria.csv', index=False)
    save_bar(df4, 'subcategoria', 'desconto_medio', 'Desconto Médio por Subcategoria', 'desconto_por_subcategoria.png')

    # Pergunta 5 - mapa
    df5 = run_query(conn, queries['avg_sale_by_country'], params)
    df5.to_csv(OUT / 'valor_medio_por_pais.csv', index=False)
    # Tentar gerar choropleth com plotly
    try:
        fig = px.choropleth(df5, locations='pais', locationmode='country names', color='valor_medio_venda', title='Valor Médio de Venda por País')
        mapa_html = OUT / 'mapa_valor_medio.html'
        fig.write_html(mapa_html)
        print(f"Mapa salvo: {mapa_html}")
    except Exception as e:
        print("Falha ao gerar mapa interactivo:", e)

    conn.close()


if __name__ == '__main__':
    main()
