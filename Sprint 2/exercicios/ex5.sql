-- o nome dos autores que publicaram livros através de editoras NÃO situadas na região sul do Brasil.
SELECT
	a.nome
FROM 
	autor a
INNER JOIN livro l ON l.autor = a.codautor
INNER JOIN editora e ON l.editora = e.codeditora
INNER JOIN endereco en ON e.endereco = en.codendereco
WHERE en.estado != 'RIO GRANDE DO SUL' AND en.estado != 'PARANÁ'
GROUP BY a.codautor
ORDER BY a.nome asc