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
    print(f"O cliente{novo_cliente["nome"]} está cadastrado com sucesso!")


def listar_clientes(cliente):
    if not clientes:
        print("Não há cliente cadastrado")
        return
    print("Lista de clientes:")
    for cpf_cliente, dados in clientes.items():
        print(f"""CPF: {cpf_cliente}
              Nome: {dados["nome"]},
              Idade: {dados["idade"]},
              Compras: {dados["compras"]},
              Categoria: {dados["categoria"]}""")


def bucar_cliente(cpf_cliente):
    if cpf_cliente in clientes:
        cliente_buscar = input("Digite o nome do cliente que deseja buscar:")
        print("Cliente está cadastrado no sistema")
    else:
        print("Cliente não está cadastrado no cliente")


while True:
    print("Cadastro de clientes Fikelinduh")
    print("1-Cadastrar clientes")
    print("2-Listar clientes")
    print("3-Buscar clientes")
    print("4-Atualizar clientes")
    print("5-Remover clientes")
    print("6-Compras")
    print("0-Sair")
    opção = input("Digite o número da opção:")
    if opção == "1":
        cadastrar_cliente()
    elif opção == "2":
        listar_clientes()
