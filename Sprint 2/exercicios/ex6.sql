-- o autor com maior número de livros publicados.
SELECT
	a.codautor, a.nome, COUNT(l.titulo) as quantidade_publicacoes
FROM
	autor a
LEFT OUTER JOIN livro l ON a.codautor = l.autor
GROUP BY a.codautor
ORDER BY quantidade_publicacoes DESC
LIMIT 1