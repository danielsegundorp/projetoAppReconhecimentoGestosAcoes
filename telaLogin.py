import os
import telaMenu
import getpass
os.system('cls')

def fazer_login():
    print("|=-=-=-= RECONHECIMENTO DE GESTOS E AÇÕES -=-=-=-|")
    print("|-=-=-=-=-=-=-=-= Tela de Login -=-=-=-=-=-=-=-=-|")
    username =           input("Usuário: ")
    password = getpass.getpass("Senha..: ")
    print("Campo de usuário preenchido: " + "*" * len(username))
    print("Campo de senha preenchido..: " + "*" * len(password))

    # Verificar se as credenciais são válidas
    if username == "admin" and password == "senha123":
        print("Login bem-sucedido!")
        telaMenu.main()
    else:
        print("Credenciais inválidas. Tente novamente.")

def main():
    while True:
        fazer_login()
        opcao = input("Deseja tentar fazer login novamente? (s/n): ")
        try:
            if opcao.lower() not in ["s", "n"]:
                raise ValueError("Opção inválida. Digite 's' para tentar novamente ou 'n' para sair.")
        except ValueError as error:
            print(error)
        else:
            if opcao.lower() == "n":
                telaMenu.sair()
                break


if __name__ == "__main__":
    main()




