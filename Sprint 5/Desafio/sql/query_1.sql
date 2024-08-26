SELECT 
    MAX(CAST("Quantidade (m3)" AS FLOAT)), 
    MIN(CAST("Quantidade (m3)" AS FLOAT))
FROM 
    S3Object
WHERE
    CAST("Quantidade (m3)" AS FLOAT) > 0
AND 
    Mes = '1'
LIMIT 100