# Análise de Viagens a Serviço — Portal da Transparência

## Sobre o projeto

Projeto de análise de dados desenvolvido em Python e PostgreSQL para investigar gastos públicos relacionados a viagens a serviço. O objetivo é transformar arquivos CSV em dados estruturados, aplicar regras de limpeza e tipagem e produzir análises que apoiem a interpretação dos gastos.

O projeto utiliza a arquitetura Medallion, organizada em três camadas: Raw, Silver e Gold.

## Tecnologias utilizadas

- **Python:** extração, transformação e preparação dos dados.
- **PostgreSQL:** armazenamento, integridade referencial e consultas SQL.
- **Pandas:** leitura e análise dos resultados.
- **Matplotlib:** visualização gráfica.
- **Jupyter Notebook:** documentação e execução das análises.
- **Git e GitHub:** versionamento do código.

## Arquitetura do pipeline

1. **Raw:** armazenamento dos dados de origem em tabelas com colunas textuais, preservando os valores importados dos CSVs.
2. **Silver:** conversão de datas e valores numéricos, aplicação de chaves primárias e estrangeiras e cálculo de indicadores derivados.
3. **Gold:** agregações analíticas organizadas em tabelas e views SQL para responder às perguntas de negócio.

Fluxo de execução:

`Arquivos CSV → Raw → Silver → Gold → Análises e visualizações`

## Estrutura dos arquivos

| Arquivo | Responsabilidade |
|---|---|
| `0_criar_banco.sql` | Criação do banco de dados e das tabelas Raw e Silver. |
| `1_extrair.py` | Download dos arquivos e carga dos CSVs nas tabelas Raw. |
| `2_transformar.py` | Conversão, limpeza e carga dos dados na camada Silver. |
| `3_analise.ipynb` | Consultas SQL, análises exploratórias, visualizações e conclusões. |
| `banco.py` | Funções de conexão, execução de comandos e inserção em lote. |
| `config.py` | Configurações do projeto, arquivos de entrada e conexão com o PostgreSQL. |
| `.env.example` | Modelo das variáveis de ambiente necessárias para a conexão. |
| `requirements.txt` | Dependências Python do projeto. |
| `.gitignore` | Arquivos e diretórios que não devem ser versionados. |

## Fonte e preparação dos dados

O projeto utiliza arquivos CSV referentes a viagens, pagamentos, passagens e trechos, disponibilizados para a atividade a partir de dados do Portal da Transparência.

Arquivos processados:

- `2025_Viagem.csv`
- `2025_Pagamento.csv`
- `2025_Passagem.csv`
- `2025_Trecho.csv`

A leitura considera separador ponto e vírgula (`;`), codificação Latin-1 e valores monetários com vírgula decimal. A extração trabalha em blocos para reduzir o consumo de memória.

O notebook analisa viagens com início entre 1º de janeiro e 30 de junho de 2025. As datas de término podem ultrapassar esse intervalo, conforme os registros disponíveis.

## Regras de transformação

- Conversão de datas para o tipo `DATE`.
- Conversão de valores monetários para tipos decimais.
- Conversão dos campos numéricos de acordo com sua finalidade.
- Relacionamento entre as tabelas por meio de `id_viagem`.
- Cálculo de `valor_total` como diárias + passagens + outros gastos − devoluções, considerando valores ausentes como zero.
- Cálculo de `duracao_dias` incluindo o primeiro e o último dia da viagem.
- Agregações com `JOIN`, `GROUP BY` e contagens distintas para reduzir duplicações causadas por relacionamentos entre viagens, pagamentos e trechos.

## Perguntas de negócio

As análises contemplam:

1. Qual tipo de pagamento apresenta o maior valor médio?
2. Qual meio de transporte é mais utilizado nos trechos?
3. Qual é a viagem de maior duração e qual é seu custo total registrado?
4. Quais são os cinco órgãos superiores com maior custo total?
5. Qual UF de destino aparece no maior número de trechos?
6. Qual órgão pagador desembolsou o maior valor total?
7. Quais são os três destinos com maior custo médio por viagem?

As análises utilizam consultas SQL e resultados tabulares, acompanhados de gráficos e interpretações quando aplicável.

## Principais resultados

- **Tipos de pagamento:** diárias apresentam o maior valor médio, seguidas por passagens.
- **Meios de transporte:** veículo oficial e transporte aéreo concentram a maior parte dos trechos.
- **Duração:** existem viagens com duração superior a 360 dias; duração elevada não significa necessariamente custo registrado elevado.
- **Órgãos superiores:** o Ministério da Justiça e Segurança Pública lidera o custo total entre os órgãos superiores analisados.
- **Destinos por UF:** São Paulo lidera em quantidade de trechos, seguido pelo Distrito Federal.
- **Órgãos pagadores:** o Fundo Nacional de Segurança Pública apresenta o maior total pago entre os órgãos pagadores identificados.

Os resultados refletem os registros e as regras de cálculo aplicadas ao conjunto de dados utilizado, não necessariamente o custo real completo de cada deslocamento.

## Como executar

### 1. Preparar o ambiente

1. Instale Python e PostgreSQL.
2. Crie e ative um ambiente virtual Python, se desejado.
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt


4. Configure as variáveis de ambiente conforme o arquivo .env.example
5. Confira as configurações de conexão com o PostgreSQL.

### 2. Executar o pipeline 

1. Execute 0_criar_banco.sql para criar o banco e as tabelas.
2. Execute 1_extrair.py para carregar os dados na camada Raw.
3. Execute 2_transformar.py para tratar os dados e carregar a camada Silver.
4. Abra e execute 3_analise.ipynb para realizar as análises.

Atenção: o script SQL contém comandos que recriam o banco de dados. 
Antes de executá-lo novamente, confirme se existem dados que precisam ser preservados.

## Segurança e limitações

- Não publique credenciais, senhas ou tokens.
- O arquivo `.env` deve permanecer fora do repositório.
- Utilize `.env.example` como modelo, sem incluir valores secretos.
- Os resultados dependem da qualidade e da completude dos dados de origem.
- Valores ausentes ou zerados não comprovam, isoladamente, que não houve custo real.
