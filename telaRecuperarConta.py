import psycopg2

def recuperarConta():
    # Solicitar e-mail do usuário
    email = input("Digite o e-mail associado à conta: ")

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

        # Verificar se o e-mail está registrado no banco de dados
        query = "SELECT * FROM Usuarios WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user is None:
            print("O e-mail fornecido não está registrado.")
        else:
            # Solicitar nova senha ao usuário
            nova_senha = input("Digite a nova senha: ")

            # Atualizar a senha no banco de dados
            update_query = "UPDATE usuarios SET password = %s WHERE email = %s"
            cursor.execute(update_query, (nova_senha, email))
            conn.commit()
            
            print("A senha foi atualizada com sucesso.")

    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao acessar o banco de dados: {error}")

    finally:
        # Fechar a conexão com o banco de dados
        if cursor:
            cursor.close()
        if conn:
            conn.close()
