from banco import conectar, executar, inserir_em_lote
from datetime import datetime


def converter_data(data_str):
    # Converte DD/MM/AAAA para objeto date do Python
    if not data_str or str(data_str).strip() == "":
        return None
    try:
        return datetime.strptime(str(data_str).strip(), "%d/%m/%Y").date()
    except ValueError:
        return None


def converter_decimal(valor_str):
    # Converte '1272,97' (texto) para float
    if not valor_str or str(valor_str).strip() == "":
        return None
    try:
        return float(str(valor_str).strip().replace(",", "."))
    except ValueError:
        return None


def converter_inteiro(valor_str):
    # Converte "1" (texto) para int
    try:
        return int(str(valor_str).strip())
    except ValueError:
        return None


def limpar_silver(conexao):
    # Limpa todas as tabelas Silver de uma vez para evitar erro de FK
    executar(conexao, "TRUNCATE TABLE silver_viagem, silver_pagamento, "
                      "silver_passagem, silver_trecho")


def transformar_viagem(conexao):
    # Transforma raw_viagem → silver_viagem
    print("Transformando silver_viagem...")

    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM raw_viagem")
    rows = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]

    dados_transformados = []
    for row in rows:
        dados = dict(zip(colunas, row))

        data_inicio = converter_data(dados.get("data_inicio"))
        data_fim = converter_data(dados.get("data_fim"))
        valor_diarias = converter_decimal(dados.get("valor_diarias"))
        valor_passagens = converter_decimal(dados.get("valor_passagens"))
        valor_devolucao = converter_decimal(dados.get("valor_devolucao"))
        valor_outros_gastos = converter_decimal(
            dados.get("valor_outros_gastos"))

    # valor_total = diarias + passagens + outros gastos - devolucao
        valor_total = ((valor_diarias or 0) + (valor_passagens or 0)
                       + (valor_outros_gastos or 0) - (valor_devolucao or 0))

        # Calculo de duracao_dias: data_fim - data_inicio + 1
        duracao_dias = None
        if data_inicio and data_fim:
            duracao_dias = (data_fim - data_inicio).days + 1

        dados_transformados.append((
            dados.get("id_viagem"),
            dados.get("num_proposta"),
            dados.get("situacao"),
            dados.get("viagem_urgente"),
            dados.get("cod_orgao_superior"),
            dados.get("nome_orgao_superior"),
            dados.get("nome_viajante"),
            dados.get("cargo"),
            data_inicio,
            data_fim,
            dados.get("destinos"),
            dados.get("motivo"),
            valor_diarias,
            valor_passagens,
            valor_devolucao,
            valor_outros_gastos,
            valor_total,
            duracao_dias
        ))

    sql = """
        INSERT INTO silver_viagem (
            id_viagem, num_proposta, situacao, viagem_urgente,
            cod_orgao_superior, nome_orgao_superior, nome_viajante, cargo,
            data_inicio, data_fim, destinos, motivo, valor_diarias,
            valor_passagens, valor_devolucao, valor_outros_gastos,
            valor_total, duracao_dias
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
    """

    inserir_em_lote(conexao, sql, dados_transformados)
    print(f"  silver_viagem: {len(dados_transformados)} linhas transformadas")


def transformar_pagamento(conexao):
    # Transforma raw_pagamento → silver_pagamento
    print("Transformando silver_pagamento...")

    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM raw_pagamento")
    rows = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]

    dados_transformados = []
    for row in rows:
        dados = dict(zip(colunas, row))

        valor = converter_decimal(dados.get("valor"))

        dados_transformados.append((
            dados.get("id_viagem"),
            dados.get("num_proposta"),
            dados.get("nome_orgao_pagador"),
            dados.get("nome_ug_pagadora"),
            dados.get("tipo_pagamento"),
            valor
        ))

    sql = """
        INSERT INTO silver_pagamento (
            id_viagem, num_proposta, nome_orgao_pagador, nome_ug_pagadora,
            tipo_pagamento, valor
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """

    inserir_em_lote(conexao, sql, dados_transformados)
    print(f"  silver_pagamento: {len(dados_transformados)} "
          "linhas transformadas")


def transformar_passagem(conexao):
    # Transforma raw_passagem → silver_passagem
    print("Transformando silver_passagem...")

    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM raw_passagem")
    rows = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]

    dados_transformados = []
    for row in rows:
        dados = dict(zip(colunas, row))

        valor_passagem = converter_decimal(dados.get("valor_passagem"))
        taxa_servico = converter_decimal(dados.get("taxa_servico"))
        data_emissao = converter_data(dados.get("data_emissao"))

        dados_transformados.append((
            dados.get("id_viagem"),
            dados.get("meio_transporte"),
            dados.get("pais_origem_ida"),
            dados.get("uf_origem_ida"),
            dados.get("cidade_origem_ida"),
            dados.get("pais_destino_ida"),
            dados.get("uf_destino_ida"),
            dados.get("cidade_destino_ida"),
            valor_passagem,
            taxa_servico,
            data_emissao
        ))

    sql = """
        INSERT INTO silver_passagem (
            id_viagem, meio_transporte, pais_origem_ida, uf_origem_ida,
            cidade_origem_ida, pais_destino_ida, uf_destino_ida,
            cidade_destino_ida, valor_passagem, taxa_servico,
            data_emissao
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    inserir_em_lote(conexao, sql, dados_transformados)
    print(f"  silver_passagem: {len(dados_transformados)} "
          "linhas transformadas")


def transformar_trecho(conexao):
    # Transforma raw_trecho → silver_trecho
    print("Transformando silver_trecho...")

    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM raw_trecho")
    rows = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]

    dados_transformados = []
    for row in rows:
        dados = dict(zip(colunas, row))

        origem_data = converter_data(dados.get("origem_data"))
        destino_data = converter_data(dados.get("destino_data"))
        numero_diarias = converter_decimal(dados.get("numero_diarias"))
        sequencia_trecho = converter_inteiro(dados.get("sequencia_trecho"))

        dados_transformados.append((
            dados.get("id_viagem"),
            sequencia_trecho,
            origem_data,
            dados.get("origem_uf"),
            dados.get("origem_cidade"),
            destino_data,
            dados.get("destino_uf"),
            dados.get("destino_cidade"),
            dados.get("meio_transporte"),
            numero_diarias
        ))

    sql = """
        INSERT INTO silver_trecho (
            id_viagem, sequencia_trecho, origem_data, origem_uf,
            origem_cidade, destino_data, destino_uf, destino_cidade,
            meio_transporte, numero_diarias
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    inserir_em_lote(conexao, sql, dados_transformados)
    print(f"  silver_trecho: {len(dados_transformados)} linhas transformadas")


def main():
    print("INICIANDO TRANSFORMACAO - CAMADA SILVER")
    print("=" * 60)

    conexao = None
    try:
        conexao = conectar()

        limpar_silver(conexao)
        transformar_viagem(conexao)
        transformar_pagamento(conexao)
        transformar_passagem(conexao)
        transformar_trecho(conexao)

        print("=" * 60)
        print("TRANSFORMACAO CONCLUIDA")

    except Exception as erro:
        print(f"ERRO: {erro}")
        raise
    finally:
        if conexao:
            conexao.close()


if __name__ == "__main__":
    main()
