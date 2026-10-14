from database import conexao, cursor
lancamentos = []

def carregar_lancamentos():
    lancamentos.clear()
    
    cursor.execute("""
        SELECT id, descricao, valor, categoria, tipo, data
        FROM lancamentos
    """)

    registros = cursor.fetchall()

    for registro in registros:
        lancamento = {
            "id": registro[0],
            "descricao": registro[1],
            "valor": registro[2],
            "categoria": registro[3],
            "tipo": registro[4],
            "data": registro[5]
        }

        lancamentos.append(lancamento)



def adicionar_lancamento():
    descricao = input("Digite a descrição do lançamento: ")

    while descricao == "":
        print("A descrição não pode ficar vazia.")
        descricao = input("Digite a descrição do lançamento: ")

    valor = input("Digite o valor do lançamento: ")

    while True:
        try:
            valor = float(valor)

            if valor <= 0:
                print("O valor deve ser maior que zero.")
                valor = input("Digite o valor do lançamento: ")
                continue

            break

        except ValueError:
            print("Digite um valor válido")
            valor = input("Digite o valor do lançamento: ")

    categoria = input("Digite a categoria do lançamento: ")

    while categoria == "":
        print("A categoria não pode ficar vazia.")
        categoria = input("Digite a categoria do lançamento: ")

    tipo = input("Digite o tipo do lançamento (Receita/Despesa): ")

    while tipo != "Receita" and tipo != "Despesa":
        print("Tipo inválido. Digite Receita ou Despesa.")
        tipo = input("Digite o tipo do lançamento (Receita/Despesa): ")

    
    lancamento = {
        "descricao": descricao,
        "valor": valor,
        "categoria": categoria,
        "tipo": tipo
    }

    lancamentos.append(lancamento)

    cursor.execute(
        """
        INSERT INTO lancamentos (descricao, valor, categoria, tipo, data)
        VALUES (?, ?, ?, ?, date('now', 'localtime'))
        """,
        (descricao, valor, categoria, tipo)
    )

    conexao.commit()
    lancamento["id"] = cursor.lastrowid

    print("Lançamento adicionado com sucesso!")


def listar_lancamentos():
    if not lancamentos:
        print("Nenhum lançamento cadastrado. ")
    for lancamento in lancamentos:
        print(f"Descrição: {lancamento['descricao']}")
        print(f"Valor: R$ {lancamento['valor']:.2f}")
        print(f"Categoria: {lancamento['categoria']}")
        print(f"Tipo: {lancamento['tipo']}")
        print("-" * 40)

def calcular_saldo():
    total = 0
    for lancamento in lancamentos:
        if lancamento["tipo"] == "Receita":
            total += lancamento["valor"]
        elif lancamento["tipo"] == "Despesa":
            total -= lancamento["valor"]
    return total


def ver_saldo():
    saldo_atual = calcular_saldo()
    print(f"Saldo atual: R$ {saldo_atual:.2f}")

def resumo_financeiro():
    total_receitas = 0
    total_despesas = 0
    for lancamento in lancamentos:
        if lancamento["tipo"] == "Receita":
            total_receitas = total_receitas + lancamento["valor"]
        elif lancamento["tipo"] == "Despesa":
            total_despesas = total_despesas + lancamento["valor"]
    print("===== RESUMO FINANCEIRO =====")
    print(f"Total de receitas: R${total_receitas:.2f}")
    print(f"Total de despesas: R${total_despesas:.2f}")

    saldo_final = total_receitas - total_despesas
    print(f"Saldo final: R${saldo_final:.2f}")
    return total_receitas, total_despesas, saldo_final

def excluir_lancamento():
    

    if not lancamentos:
        print("Nenhum lançamento cadastrado.")
        return
    
    for indice, lancamento in enumerate(lancamentos, start=1):
        print(indice, lancamento["descricao"])
    while True:
        try:
            escolha = int(input("Digite o número do lançamento que deseja excluir: "))

            if escolha >= 1 and escolha <= len(lancamentos):
                break
            print("Número do lançamento inválido.")
        except ValueError:
            print("Digite apenas número inteiro.")

        
    indice = escolha - 1
    lancamento = lancamentos[indice]
    

    cursor.execute(
        "DELETE FROM lancamentos WHERE id =?",
        (lancamento["id"],)
    )

    conexao.commit()

    lancamentos.pop(indice)
    print("Lançamento excluído com sucesso")

def editar_lancamento():
    
    if not lancamentos:
        print("Nenhum lançamento cadastrado.")
        return

    for indice, lancamento in enumerate(lancamentos, start=1):
        print(indice, lancamento["descricao"])

    while True:
        try:
            escolha = int(input("Digite o número do lançamento que deseja editar: "))
            if escolha >= 1 and escolha <= len(lancamentos):
                break
            print("Número de lançamento inválido.")        
        except ValueError:
            print("Digite apenas um número inteiro.")

    indice = escolha - 1
    lancamento = lancamentos[indice]

    

    novo_valor = input("Digite o novo valor: ")

    while True:
        try:
            novo_valor = float(novo_valor)

            if novo_valor <= 0:
                print("O valor deve ser maior que zero.")
                novo_valor = input("Digite o novo valor: ")
                continue

            break

        except ValueError:
            print("Digite um valor válido.")
            novo_valor = input("Digite o novo valor: ")


    lancamento["valor"] = novo_valor

    

    nova_categoria = input("Digite a nova categoria: ")

    while nova_categoria == "":
        print("A categoria não pode ficar vazia.")
        nova_categoria = input("Digite a nova categoria: ")
    lancamento["categoria"] = nova_categoria

    
    novo_tipo = input("Digite o novo tipo (Receita/Despesa): ")

    while novo_tipo != "Receita" and novo_tipo != "Despesa":
        print("Tipo inválido. Digite Receita ou Despesa.")
        novo_tipo = input("Digite o novo tipo (Receita/Despesa): ")


    lancamento["tipo"] = novo_tipo


    nova_descricao = input("Digite a nova descrição: ")
    while nova_descricao == "":
        print("A descrição não pode ficar vazia.")
        nova_descricao = input("Digite a nova descrição: ")
    lancamento["descricao"] = nova_descricao


    
    cursor.execute(
        """
        UPDATE lancamentos
        SET descricao = ?, valor = ?, categoria = ?, tipo = ?
        WHERE id = ?
        """,
        (
            lancamento["descricao"],
            lancamento["valor"],
            lancamento["categoria"],
            lancamento["tipo"],
            lancamento["id"]
        )
    )

    conexao.commit()

    print("Lançamento atualizado com sucesso!")

def salvar_lancamento(descricao, valor, categoria, tipo):
    cursor.execute(
        """
        INSERT INTO lancamentos (descricao, valor, categoria, tipo, data)
        VALUES (?, ?, ?, ?, date('now', 'localtime'))
        """,
        (descricao, valor, categoria, tipo)
    )

    conexao.commit()

    carregar_lancamentos()


def resumo_mensal(mes, ano):
    cursor.execute("""
        SELECT tipo, SUM(valor)
        FROM lancamentos
        WHERE strftime('%m', data) = ?
        AND strftime('%Y', data) = ?
        GROUP BY tipo
    """, (mes, ano))

    resultados = cursor.fetchall()

    total_receitas = 0
    total_despesas = 0

    for tipo, total in resultados:
        if tipo == "Receita":
            total_receitas = total
        elif tipo == "Despesa":
            total_despesas = total

    saldo_mensal = total_receitas - total_despesas

    return total_receitas, total_despesas, saldo_mensal


def atualizar_lancamento_web(id_lancamento, descricao, valor, categoria, tipo):
    cursor.execute(
        """
        UPDATE lancamentos
        SET descricao = ?, valor = ?, categoria = ?, tipo = ?
        WHERE id = ?
        """,
        (descricao, valor, categoria, tipo, id_lancamento),
    )

    conexao.commit()
    atualizado = cursor.rowcount > 0
    carregar_lancamentos()
    return atualizado


def excluir_lancamento_web(id_lancamento):
    """Exclui um lançamento pelo ID para a interface web."""
    cursor.execute(
        "DELETE FROM lancamentos WHERE id = ?",
        (id_lancamento,),
    )

    conexao.commit()
    excluido = cursor.rowcount > 0
    carregar_lancamentos()
    return excluido
