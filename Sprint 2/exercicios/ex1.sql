-- todos os livros publicados após 2014.

SELECT 
	cod, titulo, autor, editora, valor, publicacao, edicao, idioma
FROM
	livro as l
WHERE DATE(l.publicacao) > DATE('2014-12-25') 
ORDER BY l.cod ASC
