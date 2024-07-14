-- os 10 livros mais caros
SELECT 
	titulo, valor
FROM
	livro as l
ORDER BY l.valor desc
LIMIT 10