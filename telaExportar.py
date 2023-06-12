import psycopg2
import json
import zipfile

def exportarDados(id_usuario):
    # Configurações de conexão com o banco de dados
    db_host = 'localhost'
    db_port = 5432
    db_name = 'projetoB2'
    db_user = 'postgres'
    db_password = 'password'

    try:
        # Estabelecer a conexão com o banco de dados
        conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
        cursor = conn.cursor()

        # Consulta SQL para obter os dados das tabelas "acoes" e "gestos" do usuário atual
        query = """
        SELECT nome, descricao
        FROM acoes
        WHERE usuarioid = %s
        """
        cursor.execute(query, (id_usuario,))
        dados_acoes = cursor.fetchall()

        query = """
        SELECT nome, descricao
        FROM gestos
        WHERE usuarioid = %s
        """
        cursor.execute(query, (id_usuario,))
        dados_gestos = cursor.fetchall()

        # Verificar se existem dados a serem exportados
        if not dados_acoes and not dados_gestos:
            print("Nenhum dado para exportar.")
            return

        # Converter os dados para o formato JSON
        dados = {
            "acoes": dados_acoes,
            "gestos": dados_gestos
        }
        dados_json = json.dumps(dados)

        # Criar o arquivo ZIP e adicionar o arquivo JSON
        arquivo_zip = "C:/Codigos/projetoB2Topicos/dados.zip"
        with zipfile.ZipFile(arquivo_zip, "w") as zipf:
            zipf.writestr("dados.json", dados_json)

        print("Os dados foram exportados com sucesso.")

    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao acessar o banco de dados: {error}")

    finally:
        # Fechar a conexão com o banco de dados
        if cursor:
            cursor.close()
        if conn:
            conn.close()
