-- o gasto médio por estado da federação
SELECT 
estado, ROUND(AVG(qtd * vrunt), 2) gastomedio
FROM
	tbvendas t
WHERE t.status = 'Concluído'
GROUP BY estado
ORDER BY gastomedio desc