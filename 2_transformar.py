from banco import conectar, executar, inserir_em_lote
from datetime import datetime

def converter_data(data_str): 
    #Converte DD/MM/AAAA para objeto date do Python
    if not data_str or str(data_str).strip() == "":
        return None 
    try: 
        return datetime.strptime(str(data_str).strip(), "%d/%m/%Y").date()
    except ValueError: 
        return None

def converter_decimal(valor_str):
    #Converte '1272,97' (texto) para float
    if not valor_str or str(valor_str).strip() == "":
        return None
    try: 
        return float(str(valor_str).strip().replace(",", "."))
    except ValueError: 
        return None 

def limpar_silver(conexao): 
    # Limpa todas as tabelas Silver de uma vez para evitar erro de FK 
    executar(conexao, "TRUNCATE TABLE silver_viagem, silver_pagamento, "
             "silver_passagem, silver_trecho")

def transformar_viagem(conexao): 
    # Transforma raw_viagem - silver_viagem
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
        valor_outros_gastos = converter_decimal(dados.get("valor_outros_gastos"))

# Calculo do valor_total: diarias + passagens + outros gastos - devolucao
        valor_total = ((valor_diarias or 0) + (valor_passagens or 0)
               + (valor_outros_gastos or 0) - (valor_devolucao or 0))
        
# Calculo de duração_dias: data_fim - data_inicio + 1 (inclui dia inicial e final)
        duracao_dias = (data_fim - data_inicio).days + 1 if data_inicio and data_fim else None

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

    # REMOVIDO O TRUNCATE daqui - agora é feito na limpar_silver()
    
    sql = """
        INSERT INTO silver_viagem(
        id_viagem, num_proposta, situacao, viagem_urgente, 
        cod_orgao_superior, 
                        nome_orgao_superior, nome_viajante, cargo, data_inicio, data_fim, 
                        destinos, motivo, valor_diarias, valor_passagens, valor_devolucao, 
                        valor_outros_gastos, valor_total, duracao_dias  
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    inserir_em_lote(conexao, sql, dados_transformados)
    print(f"  silver_viagem: {len(dados_transformados)} linhas transformadas")
    
def main(): 
    print("INICIANDO TRANSFORMACAO - CAMADA SILVER")
    print('=' *60)

    conexao = None
    try:
        conexao = conectar()

        limpar_silver(conexao)
        transformar_viagem(conexao)

        print("=" *60)
        print("TRANSFORMACAO CONCLUIDA")

    except Exception as erro:
        print(f" ERRO: {erro}")
       
        raise
    finally: 
        if conexao: 
            conexao.close()

if __name__ == "__main__": 
    main()
