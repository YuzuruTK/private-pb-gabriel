-- os códigos das vendas identificadas como deletadas
SELECT 
t.cdven 
FROM
	tbvendas t
WHERE t.deletado = 1