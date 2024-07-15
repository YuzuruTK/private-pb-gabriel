-- a quantidade média vendida de cada produto agrupado por estado da federação
SELECT 
	t.estado, t.nmpro, ROUND(AVG(t.qtd), 4) as quantidade_media
FROM
	tbvendas t
WHERE t.status = 'Concluído'
GROUP BY t.estado, t.nmpro
ORDER BY t.estado, t.nmpro