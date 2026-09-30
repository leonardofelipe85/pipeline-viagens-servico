import gdown 
import zipfile
from config import PASTA_DADOS, DRIVE_FILE_ID 

def baixar_dados():
    # 1. Criar a pasta data (se nao existir)
    PASTA_DADOS.mkdir(exist_ok=True)

    # 2. Definir o caminho do zip (dentro da PASTA_DADOS)
    caminho_zip = PASTA_DADOS / "dados.zip"

    # 3. Baixar o zip do Drive usando o ID importado do config.py
    gdown.download(id=DRIVE_FILE_ID, output=str(caminho_zip))

    # 4. Extrair os CSVs na mesma pasta
    with zipfile.ZipFile(caminho_zip) as zip_ref:
        zip_ref.extractall(PASTA_DADOS)


if __name__ == "__main__":
    baixar_dados()