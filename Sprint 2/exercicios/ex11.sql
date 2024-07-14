--  código e nome cliente com maior gasto na loja.
SELECT 
	cdcli, nmcli, SUM(qtd * vrunt) as gasto
FROM
	tbvendas v
GROUP BY cdcli
ORDER BY gasto DESC
LIMIT 1