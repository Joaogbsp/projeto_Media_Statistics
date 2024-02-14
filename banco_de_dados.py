import sqlite3 
import datetime
# CRIAR BANCO DE DADOS REFERENTE AOS PROCESSOS
conexao = sqlite3.connect('tempo_processo.db')

cursor=conexao.cursor()

cursor.execute('''
           CREATE TABLE IF NOT EXISTS processo (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           nome_processo TEXT,
           tempo_fim TEXT,
           tempo_inicio TEXT
           )
               ''')
conexao.commit()
conexao.close()

def inserir_dados(nome_processo, tempo_fim, tempo_inicio):
    conexao = sqlite3.connect('tempo_processo.db')
    cursor=conexao.cursor()
    tempo_fim = tempo_fim.strftime('%Y-%m-%d %H:%M:%S')
    tempo_inicio = tempo_inicio.strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO processo (nome_processo, tempo_inicio, tempo_fim)
        VALUES (?, ?, ?)
    ''', (nome_processo, tempo_inicio, tempo_fim))
    conexao.commit()
    conexao.close()
