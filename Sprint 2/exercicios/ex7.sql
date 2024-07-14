-- o nome dos autores com nenhuma publicação.
SELECT 
	nome
FROM
(
SELECT
	a.nome, count(l.titulo) AS Quantidade
FROM
	autor a
LEFT OUTER JOIN livro l ON a.codautor = l.autor
GROUP BY a.codautor
)
WHERE Quantidade == 0
ORDER BY nome asc