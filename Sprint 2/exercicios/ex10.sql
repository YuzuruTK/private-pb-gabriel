-- calcule a comissão de todos os vendedores, considerando todas as vendas armazenadas na base de dados
SELECT
	t.nmvdd, ROUND(SUM(v.qtd * v.vrunt),2) as valor_total_vendas, ROUND(SUM((v.qtd * v.vrunt * t.perccomissao))/100,2) as comissao, t.perccomissao 
FROM
	tbvendas v
RIGHT OUTER JOIN tbvendedor t ON t.cdvdd = v.cdvdd 
WHERE v.status = 'Concluído'
GROUP BY v.cdvdd
ORDER BY valor_total_vendas desc
