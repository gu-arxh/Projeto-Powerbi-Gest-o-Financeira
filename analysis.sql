-- name: total_sales
-- Parâmetros opcionais: :year, :segment, :country
SELECT SUM(Total_Vendas) AS total_vendido
FROM sales
WHERE (:year IS NULL OR Ano = :year)
  AND (:segment IS NULL OR Segmento = :segment)
  AND (:country IS NULL OR Pais = :country);

-- name: sales_by_category
SELECT Categoria AS categoria, COUNT(*) AS qtd_vendas, SUM(Total_Vendas) AS valor_vendas
FROM sales
WHERE (:year IS NULL OR Ano = :year)
  AND (:segment IS NULL OR Segmento = :segment)
  AND (:country IS NULL OR Pais = :country)
GROUP BY Categoria
ORDER BY qtd_vendas DESC;

-- name: sales_by_country_priority
SELECT Pais AS pais, Prioridade AS prioridade, COUNT(*) AS qtd_vendas
FROM sales
WHERE (:year IS NULL OR Ano = :year)
  AND (:segment IS NULL OR Segmento = :segment)
  AND (:country IS NULL OR Pais = :country)
GROUP BY Pais, Prioridade
ORDER BY Pais, prioridade;

-- name: avg_discount_by_subcategory
SELECT SubCategoria AS subcategoria, AVG(Desconto) AS desconto_medio
FROM sales
WHERE (:year IS NULL OR Ano = :year)
  AND (:segment IS NULL OR Segmento = :segment)
  AND (:country IS NULL OR Pais = :country)
GROUP BY SubCategoria
ORDER BY desconto_medio DESC;

-- name: avg_sale_by_country
SELECT Pais AS pais, AVG(Total_Vendas) AS valor_medio_venda
FROM sales
WHERE (:year IS NULL OR Ano = :year)
  AND (:segment IS NULL OR Segmento = :segment)
  AND (:country IS NULL OR Pais = :country)
GROUP BY Pais
ORDER BY valor_medio_venda DESC;
