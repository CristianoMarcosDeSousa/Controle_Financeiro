

from lancamentos import(
    lancamentos,
    carregar_lancamentos,
    adicionar_lancamento,
    listar_lancamentos,
    calcular_saldo,
    ver_saldo,
    resumo_financeiro,
    excluir_lancamento,
    editar_lancamento
)

carregar_lancamentos()

while True:

    print("========== CONTROLE FINANCEIRO ==========")
    print("1 - Adicionar lançamento")
    print("2 - Listar lançamentos")
    print("3 - Ver saldo")
    print("4 - Excluir lançamento")
    print("5 - Editar lançamento")
    print("6 - Resumo financeiro")
    print("7 - Sair")
    

    opcao = input("Escolha uma opção: ")

    while opcao not in ["1", "2", "3", "4", "5", "6", "7"]:
        print("Opção inválida!")
        opcao = input("Escolha uma opção: ")

    if opcao == "1":
        adicionar_lancamento()

    elif opcao == "2":
        listar_lancamentos()

    elif opcao == "3":
        ver_saldo()

    elif opcao == "4":
        excluir_lancamento()

    elif opcao == "5":
        editar_lancamento()

    elif opcao == "6":
        resumo_financeiro()

    elif opcao == "7":
        print("Programa encerrado.")
        break