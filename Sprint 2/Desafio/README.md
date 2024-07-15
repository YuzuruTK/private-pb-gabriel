# Etapas

Foi dado o arquivo de banco de dados (`concessionaria.sqlite`) contendo uma tabela não normalizada. Para manter uma atomização e melhor manipulação dos dados, foi necessária a normalização da tabela nas 3 formas normais. Após normalizar as tabelas, também foi pedido para criar um modelo dimensional para análise.

## Normalização

A ideia principal da normalização é a atomização e redução de espaço no banco de dados, tendo assim menos informações repetidas em tabelas, o que permite uma maior organização do banco. Portanto, foram realizados os seguintes passos para normalizar o banco nas 3 formas normais:

1. Separação entre os atributos que dependiam diretamente da chave primária e dos atributos que dependiam de outra chave.
2. Com os atributos dependentes identificados, foi feita a separação entre tabelas, criando uma tabela para cada "chave primária" apresentada na tabela `tb_locacao`.
3. Após a separação, identifiquei que ainda existiam redundâncias de dados entre algumas tabelas, então foram criadas mais tabelas para uma atomização dos dados.

## Modelagem Dimensional

A ideia de um modelo dimensional é estatística, permitindo analisar os dados de diferentes formas. Normalmente, restrições de chave e uma grande quantidade de tabelas ligadas entre si podem afetar o desempenho do banco durante as consultas. Como a ideia deste modelo é exclusivamente para consultas analíticas, foi utilizado o modelo estrela, assim como a junção de algumas tabelas do modelo relacional em "dimensões", para ter o menor número de ligações entre tabelas, desconsiderando a tabela fato com as dimensões.

1. Identifiquei as tabelas que poderiam se unir, tendo como principal objetivo a unificação de uma informação, por exemplo, todas as informações do cliente na dimensão cliente.
2. Após identificar as tabelas, e ignorando alguns fatores como ligações entre tabelas de localidades (país, estado e cidade), adicionei essas informações dentro da dimensão para reduzir o tempo de processamento nas ligações entre outras tabelas, mantendo a coerência da informação, mas perdendo um pouco da atomicidade.
3. Criação da tabela de fatos com apenas dados métricos e chaves estrangeiras para questões analíticas.

# Arquivos de Entrega

1. Modelo Relacional
   - [Script SQL](entregas/relacional.sql)
   - [Imagem do Modelo](../evidencias/desafio_modelo_relacional.png)
2. Modelo Dimensional
   - [Script SQL](entregas/dimensional.sql)
   - [Imagem do Modelo](../evidencias/desafio_modelo_dimensional.png)
