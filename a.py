import sqlite3
import os

# Função para criar o banco de dados SQLite e tabelas
def criar_banco_dados():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()

    # Tabela Pessoa
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Pessoa (
        CPF TEXT PRIMARY KEY,
        PrimeiroNome TEXT,
        NomeMeio TEXT,
        Sobrenome TEXT,
        Idade INTEGER,
        ContaBancaria INTEGER
    )
    ''')

    # Tabela Conta Bancária
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ContaBancaria (
        Agencia TEXT,
        Numero TEXT PRIMARY KEY,
        Saldo REAL,
        Gerente TEXT,
        Titular TEXT
    )
    ''')

    conn.commit()
    conn.close()


# Função para preencher tabelas a partir de um arquivo .txt
def preencher_tabelas_de_arquivo():
    with open('dados.txt', 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            # Substituir espaços por vírgulas e dividir os valores em uma lista
            dados = linha.strip().replace(' ', ',').split(',')
            
            # Descompactar a lista em variáveis individuais
            cpf, primeiro_nome, nome_meio, sobrenome, idade, conta_bancaria = dados
            
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO Pessoa (CPF, PrimeiroNome, NomeMeio, Sobrenome, Idade, ContaBancaria)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (cpf, primeiro_nome, nome_meio, sobrenome, idade, conta_bancaria))
            conn.commit()
            conn.close()

# Função para adicionar uma pessoa ao banco de dados
def adicionar_pessoa(cpf, primeiro_nome, nome_meio, sobrenome, idade, conta_bancaria):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Pessoa (CPF, PrimeiroNome, NomeMeio, Sobrenome, Idade, ContaBancaria)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (cpf, primeiro_nome, nome_meio, sobrenome, idade, conta_bancaria))
    conn.commit()
    conn.close()

# Função para remover uma pessoa do banco de dados por CPF
def remover_pessoa(cpf):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Pessoa WHERE CPF = ?', (cpf,))
    conn.commit()
    conn.close()

# Função para editar os dados de uma pessoa no banco de dados
def editar_pessoa(cpf, novo_primeiro_nome, novo_nome_meio, novo_sobrenome, nova_idade, nova_conta_bancaria):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE Pessoa
    SET PrimeiroNome=?, NomeMeio=?, Sobrenome=?, Idade=?, ContaBancaria=?
    WHERE CPF=?
    ''', (novo_primeiro_nome, novo_nome_meio, novo_sobrenome, nova_idade, nova_conta_bancaria, cpf))
    conn.commit()
    conn.close()

# Função para consultar pessoas e salvar os resultados em um arquivo de texto
def consultar_pessoas_por_nome(nome):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pessoa WHERE PrimeiroNome = ?', (nome,))
    resultados = cursor.fetchall()
    conn.close()
    
    # Cria a pasta Nomes se não existir no diretório atual
    if not os.path.exists('Nomes'):
        os.mkdir('Nomes')
    
    with open(f'Nomes/{nome}.txt', 'w') as arquivo:
        for resultado in resultados:
            arquivo.write(','.join(map(str, resultado)) + '\n')

# Função para consultar pessoas por saldo e salvar os resultados em um arquivo de texto
def consultar_pessoas_por_saldo(saldo_minimo):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Pessoa INNER JOIN ContaBancaria ON Pessoa.ContaBancaria = ContaBancaria.Numero WHERE ContaBancaria.Saldo >= ?', (saldo_minimo,))
    resultados = cursor.fetchall()
    conn.close()
    
    # Cria a pasta Saldo se não existir no diretório atual
    if not os.path.exists('Saldo'):
        os.mkdir('Saldo')
    
    with open(f'Saldo/saldo_{saldo_minimo}.txt', 'w') as arquivo:
        for resultado in resultados:
            arquivo.write(','.join(map(str, resultado)) + '\n')

# Criar o banco de dados e tabelas
criar_banco_dados()

# Preencher as tabelas a partir do arquivo .txt
preencher_tabelas_de_arquivo()

# Exemplo de uso das funções
# adicionar_pessoa('125.421.431-23', 'ead', 'da', 'gh', 3, '21')
remover_pessoa('125.421.431-23')
remover_pessoa('134.422.431-61')
consultar_pessoas_por_nome('Cici')
consultar_pessoas_por_saldo(1000.00)
