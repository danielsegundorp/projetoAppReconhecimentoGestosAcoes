import psycopg2
import re

def cadastro():
    print("\n")
    print("CADASTRO NOVO USUÁRIO -=-=-=-=-=-=-=-=-=-=-=-=-=-|")
    nome = input("Digite seu nome: ")
    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")

    # Verificar se os campos são vazios
    if nome.strip() == "" or email.strip() == "" or senha.strip() == "":
        print("Usuario não cadastrado, os campos NOME, EMAIL e SENHA são obrigatórios o preenchimento.")
        return

    # Validar o formato de e-mail
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("O email inserido não possui um formato válido.")
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

        # Executar a inserção dos dados na tabela "Usuarios"
        query = "INSERT INTO Usuarios (nome, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (nome, email, senha))

        # Confirmar as alterações no banco de dados
        conn.commit()

        print("\nCadastro realizado com sucesso!")
    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao cadastrar no banco de dados: {error}")
    finally:
        # Fechar a conexão com o banco de dados
        if cursor:
            cursor.close()
        if conn:
            conn.close()
