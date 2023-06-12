import os
import telaMenu
import telaCadastro
import telaMenu
import telaSobre
import telaRecuperarConta
os.system('cls')


def menu():
    print("\n")
    print("RECONHECIMENTO DE GESTOS E AÇÕES -=-=-=-=-=-=-=-=|")
    print("1.Login Usuário...................:              |")
    print("2.Novo Usuário?...................:              |")
    print("3.ABOUT US........................:              |")
    print("4.ESQUECEU A SENHA................:              |")
    print("0.Fechar Programa.................:              |")
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-|")


def opcao1():
    print("\n")
    telaMenu.fazerLogin()
    telaMenu.main()


def opcao2():
    telaCadastro.cadastro()


def opcao3():
    telaSobre.sobre()

def opcao4():
    telaRecuperarConta.recuperarConta()

    


def fechar():
    print("fechando programa...")
    exit()

def main():
    while True:
        menu()
        opcao = input("Digite o número da opção desejada: ")

        if opcao == '1':
            opcao1()
        elif opcao == '2':
            opcao2()
        elif opcao == '3':
            opcao3()
        elif opcao == '4':
            opcao4()
        elif opcao == '0':
            fechar()
        else:
            print("Opção inválida. Tente novamente dentre as opções acima ou digite 0 para fechar:")
        

if __name__ == "__main__":
    main()




