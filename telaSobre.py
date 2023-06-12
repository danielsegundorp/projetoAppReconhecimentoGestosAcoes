import os
os.system('cls')

def sobre():
    print("\n")
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= ABOUT US -=-=-=-=-==-==-=-=-=-=-=-=-=-=-=|")
    print("TEMA..........: Reconhecimento de Gestos e Ações                        |")
    print("OBJETIVO......: Automação de comandos e tarefas através de um aplicativo|")
    print("DESENVOLVEDOR.: Daniel Segundo de Carvalho                              |")
    print("COD. MATRÍCULA: 2840482213030                                           |")
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=|")
    while True:
        opcao = input("Digite '0' para sair: ")
        if opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente")