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

