DROP DATABASE IF EXISTS transparencia WITH (FORCE);
CREATE DATABASE transparencia;
\c transparencia

CREATE TABLE raw_viagem (
    id_viagem VARCHAR(20),
    num_proposta VARCHAR(20),
    situacao VARCHAR(50),
    viagem_urgente VARCHAR(5),
    justificativa_urgencia VARCHAR(4000),
    cod_orgao_superior	VARCHAR(20), 
    nome_orgao_superior	VARCHAR(255),
    cod_orgao_solicitante	VARCHAR(20),
    nome_orgao_solicitante	VARCHAR(255),
    cpf_viajante	VARCHAR(20),
    nome_viajante	VARCHAR(255),
    cargo	VARCHAR(255),
	funcao	VARCHAR(50),
	descricao_funcao	VARCHAR(255),
	data_inicio	VARCHAR(20),
	data_fim	VARCHAR(20),
	destinos	VARCHAR(4000),
	motivo	VARCHAR(4000),
	valor_diarias	VARCHAR(20),
	valor_passagens	VARCHAR(20),
	valor_devolucao	VARCHAR(20),
	valor_outros_gastos	VARCHAR(20)
    );

CREATE TABLE raw_pagamento (
    id_viagem	VARCHAR(20), 
    num_proposta	VARCHAR(20),
	cod_orgao_superior	VARCHAR(20),
	nome_orgao_superior	VARCHAR(255),
	cod_orgao_pagador	VARCHAR(20),
	nome_orgao_pagador	VARCHAR(255),
	cod_ug_pagadora	VARCHAR(20),
	nome_ug_pagadora	VARCHAR(255),
	tipo_pagamento	VARCHAR(50),
	valor	VARCHAR(20)
);

CREATE TABLE raw_passagem (
    id_viagem	VARCHAR(20),
	num_proposta	VARCHAR(20),
	meio_transporte	VARCHAR(50),
	pais_origem_ida	VARCHAR(60),
	uf_origem_ida	VARCHAR(40),
	cidade_origem_ida	VARCHAR(80),
	pais_destino_ida	VARCHAR(60),
	uf_destino_ida	VARCHAR(40),
	cidade_destino_ida	VARCHAR(80),
	pais_origem_volta	VARCHAR(60),
	uf_origem_volta	VARCHAR(40),
	cidade_origem_volta	VARCHAR(80),
	pais_destino_volta	VARCHAR(60),
	uf_destino_volta	VARCHAR(40),
	cidade_destino_volta	VARCHAR(80),
	valor_passagem	VARCHAR(20),
	taxa_servico	VARCHAR(20),
	data_emissao	VARCHAR(20),
	hora_emissao	VARCHAR(20)
);

CREATE TABLE raw_trecho(
    id_viagem	VARCHAR(20),
	num_proposta	VARCHAR(20),
	sequencia_trecho	VARCHAR(10),
	origem_data	VARCHAR(20),
	origem_pais	VARCHAR(60),
	origem_uf	VARCHAR(40),
	origem_cidade	VARCHAR(80),
	destino_data	VARCHAR(20),
	destino_pais	VARCHAR(60),
	destino_uf	VARCHAR(40),
	destino_cidade	VARCHAR(80),
	meio_transporte	VARCHAR(50),
	numero_diarias	VARCHAR(20),
	missao	VARCHAR(10)
);

CREATE TABLE silver_viagem (
    id_viagem	VARCHAR(20) PRIMARY KEY NOT NULL, 
    num_proposta	VARCHAR(20),
	situacao	VARCHAR(50),
	viagem_urgente	VARCHAR(5),
	cod_orgao_superior	VARCHAR(20),
	nome_orgao_superior	VARCHAR(255) NOT NULL,
	nome_viajante	VARCHAR(255),
	cargo	VARCHAR(255),
	data_inicio	DATE,
	data_fim	DATE,
	destinos	VARCHAR(4000),
	motivo	VARCHAR(4000),
	valor_diarias	DECIMAL(10,2) CHECK (valor_diarias >= 0), 
	valor_passagens	DECIMAL(10,2),
	valor_devolucao	DECIMAL(10,2),
	valor_outros_gastos	DECIMAL(10,2),
	valor_total	DECIMAL(12,2),
	duracao_dias	INT
);

CREATE TABLE silver_pagamento(
    id_pagamento	SERIAL PRIMARY KEY,
	id_viagem	VARCHAR(20) NOT NULL REFERENCES silver_viagem(id_viagem),
	num_proposta	VARCHAR(20),
	nome_orgao_pagador	VARCHAR(255),
	nome_ug_pagadora	VARCHAR(255),
	tipo_pagamento	VARCHAR(50) NOT NULL,
	valor	DECIMAL(10,2) CHECK (valor >= 0)
);

CREATE TABLE silver_passagem (
    id_passagem	SERIAL PRIMARY KEY,
	id_viagem	VARCHAR(20) NOT NULL REFERENCES silver_viagem(id_viagem),
	meio_transporte	VARCHAR(50),
	pais_origem_ida	VARCHAR(60),
	uf_origem_ida	VARCHAR(40),
	cidade_origem_ida	VARCHAR(80),
	pais_destino_ida	VARCHAR(60),
	uf_destino_ida	VARCHAR(40),
	cidade_destino_ida	VARCHAR(80),
	valor_passagem	DECIMAL(10,2) CHECK (valor_passagem >= 0),
	taxa_servico	DECIMAL(10,2) CHECK (taxa_servico >= 0),
	data_emissao	DATE
);

CREATE TABLE silver_trecho (
    id_trecho	SERIAL PRIMARY KEY, 
	id_viagem	VARCHAR(20) NOT NULL REFERENCES silver_viagem(id_viagem),
	sequencia_trecho	INT,
	origem_data	DATE,
	origem_uf	VARCHAR(40),
	origem_cidade	VARCHAR(80),
	destino_data	DATE,
	destino_uf	VARCHAR(40),
	destino_cidade	VARCHAR(80), 
	meio_transporte	VARCHAR(50),
	numero_diarias	DECIMAL(10,2) CHECK (numero_diarias >= 0), 
    UNIQUE (id_viagem, sequencia_trecho)
); 