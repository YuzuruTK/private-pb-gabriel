DROP TABLE IF EXISTS tb_cliente;

DROP TABLE IF EXISTS tb_pais;

DROP TABLE IF EXISTS tb_estado;

DROP TABLE IF EXISTS tb_cidade;

DROP TABLE IF EXISTS tb_carro;

DROP TABLE IF EXISTS tb_modelo_carro;

DROP TABLE IF EXISTS tb_marcas_carro;

DROP TABLE IF EXISTS tb_combustivel;

DROP TABLE IF EXISTS tb_vendedor;

DROP TABLE IF EXISTS tb_fatos_locacao;

-- 
-- CRIAÇÃO DAS TABELAS CLIENTE
-- 
CREATE TABLE
    tb_pais (id INTEGER PRIMARY KEY autoincrement, nome TEXT);

CREATE TABLE
    tb_estado (
        id INTEGER PRIMARY KEY autoincrement,
        nome TEXT,
        pais int,
        FOREIGN KEY (pais) REFERENCES tb_pais (id)
    );

CREATE TABLE
    tb_cidade (
        id INTEGER PRIMARY KEY autoincrement,
        nome TEXT,
        estado int,
        FOREIGN KEY (estado) REFERENCES tb_estado (id)
    );

CREATE TABLE
    tb_cliente (
        id INTEGER PRIMARY KEY autoincrement,
        nome TEXT,
        cidade INT,
        FOREIGN KEY (cidade) REFERENCES tb_cidade (id)
    );

--
-- CRIAÇÃO DAS TABELAS DE CARRO
--
CREATE TABLE
    tb_marcas_carro (id INTEGER PRIMARY KEY autoincrement, nome TEXT);

CREATE TABLE
    tb_modelo_carro (
        id INTEGER PRIMARY KEY autoincrement,
        nome TEXT,
        marca INTEGER,
        FOREIGN KEY (marca) REFERENCES tb_marcas_carro (id)
    );

CREATE TABLE
    tb_carro (
        id INTEGER PRIMARY KEY autoincrement,
        classi TEXT,
        modelo INTEGER,
        ano INTEGER,
        combustivel INTEGER,
        FOREIGN KEY (modelo) REFERENCES tb_modelo_carro (id),
        FOREIGN KEY (combustivel) REFERENCES tb_combustivel (id)
    );

--
-- CRIAÇÃO DAS TABELAS COMBUSTIVEL
--
CREATE TABLE
    tb_combustivel (id INTEGER PRIMARY KEY autoincrement, nome TEXT);

--
-- CRIAÇÃO DAS TABELAS VENDEDOR
--
CREATE TABLE
    tb_vendedor (
        id INTEGER PRIMARY KEY autoincrement,
        nome TEXT,
        sexo boolean,
        estado INTEGER,
        FOREIGN KEY (estado) REFERENCES tb_estado (id)
    );

--
-- CRIAÇÃO TABELA LOCAÇÃO
--
CREATE TABLE
    tb_fatos_locacao (
        id INTEGER PRIMARY KEY autoincrement,
        dataLocacao TEXT,
        horaLocacao TEXT,
        dataEntrega TEXT,
        horaEntrega TEXT,
        qtdDiaria INT,
        vlrDiaria INT,
        kmCarro INT,
        cliente INTEGER,
        carro INTEGER,
        vendedor INTEGER,
        FOREIGN KEY (cliente) REFERENCES tb_cliente (id),
        FOREIGN KEY (carro) REFERENCES tb_carro (id),
        FOREIGN KEY (vendedor) REFERENCES tb_vendedor (id)
    );

--
-- Inserção de dados nas tabelas
--
INSERT INTO
    tb_pais (nome)
SELECT DISTINCT
    paisCliente
FROM
    tb_locacao;

INSERT INTO
    tb_estado (nome, pais)
SELECT DISTINCT
    tl.estadoCliente,
    tp.id
FROM
    tb_locacao tl
    INNER JOIN tb_pais tp ON tp.nome = tl.paisCliente;

INSERT INTO
    tb_cidade (nome, estado)
SELECT DISTINCT
    tl.cidadeCliente,
    te.id
FROM
    tb_locacao tl
    INNER JOIN tb_estado te ON te.nome = tl.estadoCliente;

INSERT INTO
    tb_cliente (id, nome, cidade)
SELECT DISTINCT
    tl.idCliente,
    tl.nomeCliente,
    tp.id
FROM
    tb_locacao tl
    INNER JOIN tb_cidade tp ON tp.nome = tl.cidadeCliente;

INSERT INTO
    tb_combustivel (id, nome)
SELECT
    idcombustivel,
    tipoCombustivel
FROM
    tb_locacao tl
GROUP BY
    idcombustivel;

INSERT INTO
    tb_marcas_carro (nome)
SELECT DISTINCT
    tl.marcaCarro
FROM
    tb_locacao tl;

INSERT INTO
    tb_modelo_carro (nome, marca)
SELECT DISTINCT
    tl.modeloCarro,
    tp.id
FROM
    tb_locacao tl
    INNER JOIN tb_marcas_carro tp ON tp.nome = tl.marcaCarro;

INSERT INTO
    tb_carro (id, classi, modelo, ano, combustivel)
SELECT DISTINCT
    tl.idCarro,
    tl.classiCarro,
    tp.id,
    tl.anoCarro,
    tc.id
FROM
    tb_locacao tl
    INNER JOIN tb_modelo_carro tp ON tp.nome = tl.modeloCarro
    INNER JOIN tb_combustivel tc ON tc.id = tl.idcombustivel;

INSERT INTO
    tb_vendedor (id, nome, sexo, estado)
SELECT DISTINCT
    tl.idVendedor,
    tl.nomeVendedor,
    tl.sexoVendedor,
    te.id
FROM
    tb_locacao tl
    INNER JOIN tb_estado te ON te.nome = tl.estadoVendedor;

INSERT INTO
    tb_fatos_locacao (
        id,
        dataLocacao,
        horaLocacao,
        dataEntrega,
        horaEntrega,
        qtdDiaria,
        vlrDiaria,
        kmCarro,
        cliente,
        carro,
        vendedor
    )
SELECT
    idLocacao,
    dataLocacao,
    horaLocacao,
    dataEntrega,
    horaEntrega,
    qtdDiaria,
    vlrDiaria,
    kmCarro,
    idCliente,
    idCarro,
    idVendedor
FROM
    tb_locacao tl
GROUP BY
    idLocacao;