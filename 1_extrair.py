import gdown 
import zipfile
import pandas as pd 
from config import PASTA_DADOS, DRIVE_FILE_ID, CSV_SEPARADOR, CSV_ENCODING, TAMANHO_BLOCO, ARQUIVOS
from banco import executar, inserir_em_lote, conectar

def baixar_dados():
    # 1. Criar a pasta data (se nao existir)
    PASTA_DADOS.mkdir(exist_ok=True)

    # 2. Definir o caminho do zip (dentro da PASTA_DADOS)
    caminho_zip = PASTA_DADOS / "dados.zip"

    # 3. Baixar o zip do Drive usando o ID importado do config.py
    if not caminho_zip.exists(): 
        gdown.download(id=DRIVE_FILE_ID, output=str(caminho_zip))

    # 4. Extrair os CSVs na mesma pasta
    with zipfile.ZipFile(caminho_zip) as zip_ref:
        zip_ref.extractall(PASTA_DADOS)


def carregar_tabela(conexao, arquivo_csv, tabela): 
    # 1. Montar o caminho do csv (dentro da PASTA_DADOS)
    caminho = PASTA_DADOS / arquivo_csv

    # 2. Esvaziar a tabela raw 
    executar(conexao, f"TRUNCATE TABLE {tabela}")

    # 3. Ler o csv em blocos, sem o pandas converter nada 
    blocos = pd.read_csv(
        caminho, 
        sep=CSV_SEPARADOR, 
        encoding=CSV_ENCODING, 
        dtype=str, 
        keep_default_na=False, 
        chunksize=TAMANHO_BLOCO
    )

    # 4. Para cada bloco: montar o sql de insert e inserir 
    for bloco in blocos: 
        marcadores = ", ".join(["%s"] * len(bloco.columns))
        sql = f"INSERT INTO {tabela} VALUES ({marcadores})"
        inserir_em_lote(conexao, sql, bloco.values.tolist())  

def main(): 
    conexao = None
    try: 
        # 1. Baixar os dados 
        baixar_dados()

        # 2. Abrir a conexao com o banco 
        conexao = conectar()

        # 3. Para cada arquivo em ARQUIVOS: carregar a tabela raw e imprimir uma mensagem
        for nome, info in ARQUIVOS.items(): 
            carregar_tabela(conexao, info["csv"], info["tabela_raw"])
            print(
                f"Tabela {info['tabela_raw']} carregada com sucesso do arquivo {info['csv']}")

        # 4. imprimir que terminou
        print("Carga dos dados concluída com sucesso!")

    except Exception as erro:
        # imprimir o erro
        print(f"Erro durante a execução: {erro}")

    finally:
        # fechar a conexao
        if conexao:
            conexao.close()

if __name__ == "__main__":
    main()