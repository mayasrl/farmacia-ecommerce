import sys

from services import cadastrar_cliente, cadastrar_laboratorio, cadastrar_medicamento, realizar_venda
from relatorios.gerador_relatorios import listar_clientes, listar_todos_medicamentos, listar_medicamentos_por_tipo, exibir_estatisticas_dia

def exibir_menu():
    print("\n======== Farmácia E-Commerce ========")
    print("1. Cadastrar Cliente")
    print("2. Cadastrar Laboratório")
    print("3. Cadastrar Medicamento")
    print("4. Realizar Venda")
    print("5. Relatórios")
    print("6. Sair")
    print("=====================================")

def menu_relatorios():
    while True:
        print("\n======== Menu de Relatórios ========")
        print("1. Listar Clientes")
        print("2. Listar Todos os Medicamentos")
        print("3. Listar Medicamentos por Tipo")
        print("4. Exibir Estatísticas do Dia")
        print("5. Voltar ao Menu Principal")
        print("====================================")
        escolha_rel = input("Escolha uma opção (1-5): ").strip()

        if escolha_rel == "1":
            listar_clientes()
        elif escolha_rel == "2":
            listar_todos_medicamentos()
        elif escolha_rel == "3":
            listar_medicamentos_por_tipo()
        elif escolha_rel == "4":
            exibir_estatisticas_dia()
        elif escolha_rel == "5":
            break
        else:
            print("Opção inválida. Tente novamente.")

def main():
    print("Iniciando sistema de Farmácia E-Commerce…")
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção (1-6): ").strip()

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            cadastrar_laboratorio()
        elif opcao == "3":
            cadastrar_medicamento()
        elif opcao == "4":
            realizar_venda()
        elif opcao == "5":
            menu_relatorios()
        elif opcao == "6":
            print("Saindo do sistema. Até mais!")
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()

