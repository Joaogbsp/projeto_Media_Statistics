import psutil
import sqlite3
import time
import pygetwindow as gw

def criar_tabela():
    conn = sqlite3.connect('registro_atividades.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            processo TEXT,
            status TEXT,
            tempo_abertura DATETIME,
            tempo_encerramento DATETIME,
            duracao TEXT
        )
    ''')
    conn.commit()
    conn.close()

def obter_nome_janela_ativa():
    janela_ativa = gw.getWindowsWithTitle(gw.getActiveWindowTitle())
    if janela_ativa:
        return janela_ativa[0].title
    return None

def processo_em_execucao(processo_nome):
    for processo in psutil.process_iter(['name']):
        if processo.info['name'].lower() == processo_nome.lower():
            return True
    return False

def inserir_registro(processo, status, tempo_abertura, tempo_encerramento, duracao):
    conn = sqlite3.connect('registro_atividades.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO atividades (processo, status, tempo_abertura, tempo_encerramento, duracao) VALUES (?, ?, ?, ?, ?)',
                   (processo, status, tempo_abertura, tempo_encerramento, duracao))
    conn.commit()
    conn.close()

def monitorar_aplicativos():
    criar_tabela()

    processo_anterior = None
    tempo_abertura = None

    while True:
        nome_janela = obter_nome_janela_ativa()

        if nome_janela:
            processo_atual = nome_janela.lower()

            if processo_atual != processo_anterior:
                tempo_atual = time.strftime('%Y-%m-%d %H:%M:%S')

                if processo_anterior and not processo_em_execucao(processo_anterior):
                    tempo_encerramento = tempo_atual
                    duracao = calcular_duracao(tempo_abertura, tempo_encerramento)
                    inserir_registro(processo_anterior, 'Encerrado', tempo_abertura, tempo_encerramento, duracao)

                tempo_abertura = tempo_atual
                inserir_registro(processo_atual, 'Iniciado', tempo_abertura, None, None)

                processo_anterior = processo_atual

        time.sleep(5)

def calcular_duracao(tempo_inicial, tempo_final):
    formato = '%Y-%m-%d %H:%M:%S'
    tempo_inicial = time.mktime(time.strptime(tempo_inicial, formato))
    tempo_final = time.mktime(time.strptime(tempo_final, formato))
    duracao_segundos = tempo_final - tempo_inicial

    horas, resto = divmod(duracao_segundos, 3600)
    minutos, segundos = divmod(resto, 60)

    duracao_formatada = '{:02}:{:02}:{:02}'.format(int(horas), int(minutos), int(segundos))
    return duracao_formatada

if __name__ == "__main__":
    monitorar_aplicativos()
