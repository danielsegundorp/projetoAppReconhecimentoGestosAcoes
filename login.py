import getpass
import psycopg2 as pg2
import telaLogin

def fazerLogin():
    print("|=-=-=-= RECONHECIMENTO DE GESTOS E AÇÕES -=-=-=-|")
    print("|-=-=-=-=-=-=-=-=-=-= Login -=-=-=-=-=-=-=-=-=-=-|")
    nome = input("Usuário: ")
    password = getpass.getpass("Senha..: ")
    print("Campo de usuário preenchido: " + "*" * len(nome))
    print("Campo de senha preenchido..: " + "*" * len(password))

    # Configurações de conexão com o banco de dados
    db_host = 'localhost'
    db_port = 5432
    db_name = 'projetoB2'
    db_user = 'postgres'
    db_password = 'password'

    try:
        # Estabelece a conexão com o banco de dados
        conn = pg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
        cursor = conn.cursor()

        # Executa a consulta para verificar as credenciais do usuário
        query = "SELECT user_id FROM usuarios WHERE nome = %s AND password = %s"
        cursor.execute(query, (nome, password))
        result = cursor.fetchone()

        # Verifica se as credenciais são válidas
        if result:
            print("Login bem-sucedido!")
            id_usuario = result[0]  # Obtém o ID do usuário da primeira coluna
            return id_usuario
        else:
            print("Credenciais inválidas. Tente novamente.")
            telaLogin.main()
            return None

    except (pg2.Error, pg2.DatabaseError) as error:
        print("Erro ao fazer login:", error)

    finally:
        # Fecha a conexão com o banco de dados
        if cursor:
            cursor.close()
        if conn:
            conn.close()


