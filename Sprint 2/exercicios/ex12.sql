-- código, nome e data de nascimento dos dependentes do vendedor com menor valor total bruto em vendas (não sendo zero).

SELECT dep.cddep, dep.nmdep, dep.dtnasc, t.valor_total_vendas FROM
(
SELECT
	t.cdvdd, ROUND(SUM(v.qtd * v.vrunt),2) as valor_total_vendas 
FROM
	tbvendas v
RIGHT OUTER JOIN tbvendedor t ON t.cdvdd = v.cdvdd
INNER JOIN tbdependente dep ON dep.cdvdd = t.cdvdd
WHERE v.status = 'Concluído'
GROUP BY v.cdvdd
ORDER BY valor_total_vendas ASC
LIMIT 1
) as t
INNER JOIN tbdependente dep ON dep.cdvdd = t.cdvdd