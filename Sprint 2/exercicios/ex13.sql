-- listar os 10 produtos menos vendidos pelos canais de E-Commerce ou Matriz
SELECT 
	t.cdpro, t.nmcanalvendas, t.nmpro, SUM(t.qtd) as quantidade_vendas
FROM
	tbvendas t 
WHERE (t.nmcanalvendas = 'Matriz' OR t.nmcanalvendas = 'Ecommerce') AND t.status = 'Concluído'
GROUP BY t.cdpro, t.nmcanalvendas
ORDER BY quantidade_vendas asc
LIMIT 10