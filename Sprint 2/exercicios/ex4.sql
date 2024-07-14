-- a quantidade de livros publicada por cada autor
SELECT
	a.nome,a.codautor, a.nascimento , COUNT(l.titulo) as quantidade 
FROM
	autor a
LEFT OUTER JOIN livro l ON a.codautor = l.autor
GROUP BY a.codautor
ORDER BY a.nome asc