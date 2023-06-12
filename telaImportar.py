import json
import psycopg2
from flask import Flask, jsonify
import telaMenu

app = Flask(__name__)

# Configurações de conexão com o banco de dados
db_host = 'localhost'
db_port = 5432
db_name = 'projetoB2'
db_user = 'postgres'
db_password = 'password'

def importarDados(id_usuario):
    # Caminho do arquivo JSON local
    arquivo_json = 'C:/Codigos/projetoB2Topicos/dados/acoesGestos.json'
    confirmacao = input("Deseja importar os dados do arquivo JSON? (s/n): ")
    if confirmacao.lower() == 's':
        try:
            # Carregar os dados do arquivo JSON
            with open(arquivo_json, 'r') as file:
                dados = json.load(file)

            # Extrair os dados das tabelas "gestos" e "acoes"
            dados_gestos = dados.get("gestos", [])
            dados_acoes = dados.get("acoes", [])

            # Estabelecer a conexão com o banco de dados
            conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
            cursor = conn.cursor()

            # Importar os dados para a tabela "gestos"
            for gesto in dados_gestos:
                nome = gesto[0]
                descricao = gesto[1]
                query = "INSERT INTO gestos (nome, descricao, usuarioid) VALUES (%s, %s, %s)"
                cursor.execute(query, (nome, descricao, id_usuario))

            # Importar os dados para a tabela "acoes"
            for acao in dados_acoes:
                nome = acao[0]
                descricao = acao[1]
                query = "INSERT INTO acoes (nome, descricao, usuarioid) VALUES (%s, %s, %s)"
                cursor.execute(query, (nome, descricao, id_usuario))

            conn.commit()
            print("Os dados foram importados com sucesso.")
            # Executar o servidor Flask para disponibilizar os dados em um endereço da web
            app.run(host='0.0.0.0', port=8000)

        except (Exception, psycopg2.Error) as error:
            print(f"Erro ao acessar o banco de dados: {error}")

        finally:
            # Fechar a conexão com o banco de dados
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    elif confirmacao.lower() == 'n':
        telaMenu.main()
    else:
        print("Opção inválida. Por favor, digite 's' para importar ou 'n' para cancelar.")
        importarDados(id_usuario)

def obterDados():
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()

    # Recuperar dados da tabela "gestos"
    cursor.execute("SELECT nome, descricao FROM gestos")
    dados_gestos = cursor.fetchall()

    # Recuperar dados da tabela "acoes"
    cursor.execute("SELECT nome, descricao FROM acoes")
    dados_acoes = cursor.fetchall()

    cursor.close()
    conn.close()

    # Formatar os dados em um dicionário
    dados = {
        "gestos": dados_gestos,
        "acoes": dados_acoes
    }

    return jsonify(dados)

@app.route('/acoesGestos', methods=['GET'])
def dados():
    return obterDados()


