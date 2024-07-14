-- o código e nome do produto mais vendido entre as datas de 2014-02-03 até 2018-02-02
SELECT
	v.cdpro, v.nmpro
FROM
	tbvendas v
WHERE dtven BETWEEN '2014-02-03' AND '2018-02-02'
GROUP BY v.cdpro
ORDER BY count(v.cdpro) DESC
LIMIT 1
