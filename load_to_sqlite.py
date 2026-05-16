#!/usr/bin/env python3
"""Carrega `dataset.txt.csv` para um banco SQLite chamado `data.db`.
Uso: python load_to_sqlite.py
"""
import pandas as pd
import sqlite3
from pathlib import Path


CSV = Path("dataset.txt.csv")
DB = Path("data.db")


def load():
    if not CSV.exists():
        raise SystemExit(f"Arquivo não encontrado: {CSV}")

    # Leitura tratando ponto como separador de milhares e vírgula como decimal
    df = pd.read_csv(CSV, sep=";", decimal=",", thousands='.', parse_dates=["Data_Pedido"], dayfirst=True, engine='python')

    # Normalizar nomes de colunas (remover espaços laterais)
    df.columns = [c.strip() for c in df.columns]

    # Criar coluna Ano para filtros
    if 'Data_Pedido' in df.columns:
        df['Ano'] = pd.to_datetime(df['Data_Pedido'], dayfirst=True, errors='coerce').dt.year

    # Garantir tipos numéricos
    for col in ['Total_Vendas', 'Quantidade', 'Desconto', 'Lucro']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Gravar em SQLite
    conn = sqlite3.connect(DB)
    df.to_sql('sales', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Dados carregados em {DB} (tabela: sales). Linhas: {len(df)}")


if __name__ == '__main__':
    load()
