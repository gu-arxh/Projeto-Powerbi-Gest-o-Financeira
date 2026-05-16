# Projeto - Análises para Dashboard

Arquivos criados:

- `load_to_sqlite.py`: carrega `dataset.txt.csv` para `data.db` (tabela `sales`).
- `analysis.sql`: consultas SQL para as perguntas pedidas (suporta filtros de `year`, `segment` e `country`).
- `analyze.py`: executa as queries e gera gráficos em `outputs/` (PNG, CSV e mapa HTML).
- `requirements.txt`: dependências Python.

Como usar (ambiente Linux):

1. Instale dependências:

```bash
python3 -m pip install -r requirements.txt
```

2. Carregue os dados no SQLite:

```bash
python3 load_to_sqlite.py
```

3. Rode a análise (opcionalmente filtrando por ano, segmento e país):

```bash
python3 analyze.py --year 2014 --segment Consumidor --country "United States"
```

Saídas em `outputs/`:

- `vendas_por_categoria.png`, `vendas_por_categoria.csv`
- `vendas_por_pais_total.png`, `vendas_por_pais_prioridade.csv`
- `desconto_por_subcategoria.png`, `desconto_medio_subcategoria.csv`
- `valor_medio_por_pais.csv`, `mapa_valor_medio.html`

Observações:

- Os scripts assumem que `dataset.txt.csv` está na raiz do repositório e usa `;` como separador e vírgula como decimal.
- O mapa usa nomes de países; caso alguns nomes não sejam reconhecidos pelo plotly, confira o CSV `outputs/valor_medio_por_pais.csv` para ajustar nomes.
📊 Gestão Financeira Global - Dashboard Power BI
Dashboard interativo desenvolvido em Power BI para análise de dados financeiros globais. Contém análise de 12,64 milhões em vendas, cobrindo 50+ países, 3 categorias de produtos e 4 níveis de prioridade operacional.
Dados:

15+ anos de histórico (2011-2024)
10.000+ registros de pedidos
3 segmentos: Consumidor, Corporativo, Home Office
20+ subcategorias de produtos

Visualizações:

KPI de vendas totais
Mapa geográfico interativo com Bing Maps
Gráfico de contagem de pedidos por categoria
Análise de prioridades por categoria
Média de desconto por subcategoria
Heatmap de pedidos por país e prioridade

Tecnologias: Power BI Desktop, Excel, DAX, CSV
Filtros dinâmicos: Ano, Mês, Segmento, País
Licença MIT - Open Source.
