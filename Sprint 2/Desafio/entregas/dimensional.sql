DROP VIEW IF EXISTS fatos_locacao;

DROP VIEW IF EXISTS dim_cliente;

DROP VIEW IF EXISTS dim_carro;

DROP VIEW IF EXISTS dim_vendedor;

-- Criação da View de Fatos
CREATE VIEW
    fatos_locacao AS
SELECT
    *
FROM
    tb_fatos_locacao tfl;

-- Criação das Dimensões
-- Dimensão Cliente
CREATE VIEW
    dim_cliente AS
SELECT
    c.id,
    c.nome AS nome,
    cid.nome AS cidade,
    est.nome AS estado,
    pa.nome AS pais
FROM
    tb_cliente c
    INNER JOIN tb_cidade cid ON cid.id = c.cidade
    INNER JOIN tb_estado est ON cid.estado = est.id
    INNER JOIN tb_pais pa ON pa.id = est.pais;

-- Dimensão Carro
CREATE VIEW
    dim_carro AS
SELECT
    car.id,
    car.classi,
    car.ano,
    modc.nome AS modelo,
    marc.nome AS marca,
    comb.nome AS combustivel
FROM
    tb_carro car
    INNER JOIN tb_modelo_carro modc ON modc.id = car.modelo
    INNER JOIN tb_marcas_carro marc ON marc.id = modc.marca
    INNER JOIN tb_combustivel comb ON comb.id = car.combustivel;

-- Dimensão Vendedor
CREATE VIEW
    dim_vendedor AS
SELECT
    tv.id,
    tv.nome,
    tv.sexo,
    te.nome AS estado,
    tp.nome AS pais
FROM
    tb_vendedor tv
    INNER JOIN tb_estado te ON te.id = tv.estado
    INNER JOIN tb_pais tp ON tp.id = te.pais;