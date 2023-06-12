import psycopg2

def apagarConta(id_usuario, email, password):
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

        # Verificar se o usuário existe e a senha está correta
        query = "SELECT * FROM Usuarios WHERE user_id = %s AND email = %s AND password = %s"
        cursor.execute(query, (id_usuario, email, password))
        user = cursor.fetchone()

        if user is None:
            print("Usuário não encontrado ou senha incorreta.")
        else:
            # Excluir os registros relacionados na tabela "acoes"
            delete_acoes_query = "DELETE FROM acoes WHERE usuarioid = %s"
            cursor.execute(delete_acoes_query, (id_usuario,))

            # Excluir os registros relacionados na tabela "gestos"
            delete_acoes_query = "DELETE FROM gestos WHERE usuarioid = %s"
            cursor.execute(delete_acoes_query, (id_usuario,))
            
            # Excluir o registro do usuário na tabela "Usuarios"
            delete_usuario_query = "DELETE FROM Usuarios WHERE user_id = %s"
            cursor.execute(delete_usuario_query, (id_usuario,))
            
            conn.commit()
            print("Conta do usuário apagada com sucesso!")

    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao acessar o banco de dados: {error}")

    finally:
        # Fechar a conexão com o banco de dados
        if cursor:
            cursor.close()
        if conn:
            conn.close()
