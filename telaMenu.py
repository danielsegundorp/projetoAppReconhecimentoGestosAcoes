import os
os.system('cls')

def menu():
    print("-=-=-=-=-=-=-=-=-=-= MENU -=-=-=-=-=-=-=-=-=-=-|")
    print("1.....Cadastrar Gestos..........:              |")
    print("2.....Cadastrar Ações...........:              |")
    print("3.....Configurar Feedback.......:              |")
    print("4.....Exportar / Importar dados.:              |")
    print("5.....Apagar dados..............:              |")
    print("6.....Voltar tela Operação......:              |")
    print("7.....Sair......................:              |")
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-|")

def opcao1():
    print("-=-=-=-=-=-=-= CADASTRAR GESTOS -=-=-=-=-=-=-=-|")
    print("programa aqui...              |")

def opcao2():
    print("-=-=-=-=-=-=-= CADASTRAR AÇÕES -=-=-=-=-=-=-=-=|")
    print("programa aqui...              |")

def opcao3():
    print("-=-=-=-=-=-= CONFIGURAR FEEDBACK -=-=-=-=-=-=-=|")
    print("programa aqui...              |")

def opcao4():
    print("-=-=-=-=-= EXPORTAR / IMPORTAR DADOS -=-=-=-=-=|")
    print("programa aqui...              |")

def opcao5():
    print("-=-=-=-=-=-=-=-= APAGAR DADOS -=-=-=-=-=-=-=-=-|")
    print("programa aqui...              |")
          
def opcao6():
    print("-=-=-=-=-=-=-=- TELA OPERAÇÃO -=-=-=-=-=-=-=-=-|")
    print("programa aqui...              |")

def sair():
    print("Saindo do programa...")
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
        elif opcao == '5':
            opcao5()
        elif opcao == '6':
            opcao6()
        elif opcao == '7':
            sair()
        else:
            print("Opção inválida. Tente novamente dentre as opções acima ou digite 7 para sair:")

if __name__ == "__main__":
    main()