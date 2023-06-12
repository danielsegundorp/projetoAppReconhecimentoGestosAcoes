import psycopg2
import re

def atualizarEmail(id_usuario):
    # Solicitar novo e-mail do usuário
    print("\n")
    print("|=-=-=-=-=-= ATUALIZAR EMAIL-=-=-=-=-=-=-|")
    novo_email = input("Digite o novo e-mail: ")

    # Verificar se o e-mail é válido
    if not re.match(r"[^@]+@[^@]+\.[^@]+", novo_email):
        print("O e-mail inserido não é válido.")
        return

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

        # Atualizar o e-mail no banco de dados
        update_query = "UPDATE usuarios SET email = %s WHERE user_id = %s"
        cursor.execute(update_query, (novo_email, id_usuario))
        conn.commit()
        
        print("O e-mail foi atualizado com sucesso.")

    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao acessar o banco de dados: {error}")

    finally:
        # Fechar a conexão com o banco de dados
        if cursor:
            cursor.close()
        if conn:
            conn.close()
