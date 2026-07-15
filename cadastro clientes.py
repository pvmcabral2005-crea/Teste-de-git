clientes = {
    "32105462311": {"nome": "Paulo", "idade": 22, "compras": [35.20, 53.13], "categoria": "Regular"},
    "78420396628": {"nome": "Ana", "idade": 21, "compras": [27.15, 42.30], "categoria": "VIP"},
    "41774528155": {"nome": "George", "idade": 30, "compras": [36.40, 61.25], "categoria": "Premium"}
}


def cadastrar_cliente():
    cpf_cliente = input("Digite o CPF do cliente: ")
    novo_cliente = {}
    novo_cliente["nome"] = input("Digite o nome do cliente:")
    novo_cliente["idade"] = int(input("Digite a idade do cliente:"))
    novo_cliente["compras"] = []
    novo_cliente["categoria"] = "Regular"
    clientes[cpf_cliente] = novo_cliente
    print(f"O cliente {novo_cliente["nome"]} está cadastrado com sucesso!")


def listar_clientes():
    if not clientes:
        print("Não há cliente cadastrado")
        return clientes
    print("Lista de clientes:")
    for cpf_cliente, dados in clientes.items():
        print(f"""CPF: {cpf_cliente}
              Nome: {dados["nome"]},
              Idade: {dados["idade"]},
              Compras: {dados["compras"]},
              Categoria: {dados["categoria"]}""")


def buscar_cliente(cpf_buscar):
    if cpf_buscar in clientes:
        dados = clientes[cpf_buscar]
        print(f"O cliente foi encontrado: {dados["nome"]}")
        return dados
    else:
        print("Cliente não foi encontrado")

def atualizar_cliente():
    cpf_atualizar = input("Digite o CPF que deseja atualizar:")
    cliente = buscar_cliente(cpf_atualizar)
    if cliente:
        cliente["nome"] = input("Digite o nome do cliente:")
        cliente["idade"] = input("Digite a idade do cliente:")
        print(f"O cliente{cliente ["nome"]} está atualizado com sucesso")
def excluir_cliente():
    deletar_cpf = input("Digite o CPF do cliente que deseja excluir:")
    cliente = buscar_cliente(deletar_cpf)
    if cliente:
        del clientes[deletar_cpf]
        print("Cliente excluído")
       

def calcular_faturamento_do_cliente():
    cpf_cliente = input("Digite o CPF do cliente que quer fazer a compra:")
    cliente = buscar_cliente(cpf_cliente)
    if cliente:
        faturamento = sum(cliente["compras"])
        print(f"O faturamento total do cliente {cliente["compras"]} é R${faturamento:.2f}")
def fazer_compras():
    cpf_cliente = input("Digite o CPF do cliente que fará a compra:")
    cliente_compra = buscar_cliente(cpf_cliente)
    if cliente_compra:
        compra_valor = float(input("Digite o valor da compra do cliente:"))
        cliente_compra["compras"].append(compra_valor)

    
while True:
    print("""====Cadastro de clientes FikeLinduh====
          1-Cadastrar clientes
          2-Listar clientes
          3-Buscar cliente
          4-Atualizar cliente
          5-Excluir cliente
          6-Fazer compras
          0-Sair """)
    
    opção = input("Digite o número da opção:")
    if opção == "1":
        cadastrar_cliente()
    elif opção == "2":
        listar_clientes()
    elif opção == "3":
        cpf_cliente = input("Digite o CPF do cliente que deseja buscar:")
    elif opção == "4":
        atualizar_cliente()
    elif opção == "5":
        excluir_cliente()
    elif opção == "6":
        fazer_compras()
    else:
        print("Opção não existe.Tente novamente")
