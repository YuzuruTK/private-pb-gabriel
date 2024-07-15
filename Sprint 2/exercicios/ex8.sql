-- o código e o nome do vendedor com maior número de vendas (contagem)
SELECT 
	t.cdvdd, t.nmvdd
FROM 
	tbvendedor t 
LEFT OUTER JOIN tbvendas v ON t.cdvdd = v.cdvdd 
GROUP BY t.cdvdd
ORDER BY count(v.cdven) DESC
LIMIT 1