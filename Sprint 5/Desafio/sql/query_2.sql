SELECT
    UPPER(Cidade) || ' - ' || "Campus/Unidade", 
    CASE WHEN "Quantidade (m3)" = '0' THEN 'Nada' ELSE CAST("Quantidade (m3)" AS FLOAT) END,
    CASE WHEN CAST(mes AS INT) < 10 THEN TO_TIMESTAMP("Ano" || '-0' || "Mes" || '-01') ELSE TO_TIMESTAMP("Ano" || '-' || "Mes" || '-01') END
FROM
    S3Object
WHERE
    Cidade = 'Uberlândia'
LIMIT 100