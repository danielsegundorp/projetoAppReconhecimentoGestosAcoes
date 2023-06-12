import telaConfigAcoes
import telaLogin
import login
import telaConfigGestos
import telaApagarConta
import telaAtualizarEmail
import telaExportar
import telaImportar


id_usuario = None

def menu():
    print("-=-=-=-=-=-=-=-=-=-= MENU -=-=-=-=-=-=-=-=-=-=-|")
    print("1......Trabalhar Gestos.........:              |")
    print("2.......Trabalhar Ações.........:              |")
    print("3.....Exportar / Importar dados.:              |")
    print("4.....Apagar conta..............:              |")
    print("5.....Atualizar email...........:              |")
    print("0.....Logout....................:              |")
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-|")

def Gestos():
    global id_usuario
    if id_usuario is not None:
        telaConfigGestos.configGestos(id_usuario)
    else:
        print("Nenhum usuário logado. Faça login primeiro.")

def cadastrarAcoes():
    global id_usuario
    if id_usuario is not None:
        telaConfigAcoes.configAcoes(id_usuario)
    else:
        print("Nenhum usuário logado. Faça login primeiro.")


def exportarImportarDados():
    print("\n")
    print("EXPORTAR / IMPORTAR DADOS -=-=-=-=-=--=-=-=-=-=|")
    print("1......Exportar Dados...........:              |")
    print("2......Importar Dados...........:              |")
    option = input("Digite a sua opção: ")
    if option == '1':
        telaExportar.exportarDados(id_usuario)
    elif option == '2':
        telaImportar.importarDados(id_usuario)
    else:
        print("Opção inválida. Tente novamente dentre as opções acima ou digite 0 para sair:")

    

def apagarConta():
    global id_usuario
    if id_usuario is not None:
        email = input("Digite o email da conta a ser apagada: ")
        password = input("Digite a senha da conta a ser apagada: ")

        confirmacao = input("Tem certeza de que deseja apagar a conta? (S/N): ")
        if confirmacao.upper() == "S":
            telaApagarConta.apagarConta(id_usuario, email, password)
            logoff()
        else:
            print("Operação de exclusão da conta cancelada.")
    else:
        print("Nenhum usuário logado. Faça login primeiro.")


          
def logoff():
    global id_usuario
    id_usuario = None
    print("Logout realizado!!!.............................")
    telaLogin.main()

def fazerLogin():
    global id_usuario
    id_usuario = login.fazerLogin()


def processarOpcao(opcao):
    if opcao == '1':
        Gestos()
    elif opcao == '2':
        cadastrarAcoes()
    elif opcao == '3':
        exportarImportarDados()
    elif opcao == '4':
        apagarConta()
    elif opcao == '5':
        telaAtualizarEmail.atualizarEmail(id_usuario)
    elif opcao == '0':
        logoff()
    else:
        print("Opção inválida. Tente novamente dentre as opções acima ou digite 0 para sair:")

def main():
    while True:
        menu()
        opcao = input("Digite o número da opção desejada: ")
        processarOpcao(opcao)

       

