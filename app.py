import pygetwindow as gw
from banco_de_dados import inserir_dados
import time
from datetime import datetime
def obter_tempo_ativo():
    nome_processo =  gw.getActiveWindowTitle()
    if nome_processo is not None:
        tempo_inicio = datetime.now()
        while gw.getActiveWindowTitle() == nome_processo:
            time.sleep(10)
            tempo_fim = datetime.now()
            return nome_processo, tempo_inicio, tempo_fim
        return None, None, None   
while True:
   nome_processo, tempo_inicio, tempo_fim = obter_tempo_ativo()
   if nome_processo is not None:
       inserir_dados(nome_processo, tempo_inicio, tempo_fim)
