import time
import os

        # Função para login do usuário
        # Verifica se o nome e senha estão corretos para o cargo especificado.
def login(cargo):
    for nome, senha, _ in users[cargo]:
        if nome == user_name and senha == user_pass:
            return True
    return False

# Função para formatar valores monetários no formato brasileiro.
# Transforma o valor numérico em uma string formatada com a moeda brasileira e substitui os separadores de milhar e decimal.
def fmt_moeda(valor):
    valor = str(valor).replace("R$", "").replace(".", "").replace(",", ".")
    return f'R${float(valor):,.2f}'.replace(".", "X").replace(",", ".").replace("X", ",")

    

# Função para registrar a entrada de produtos no estoque.
# Percorre a lista de estoque e, ao encontrar o produto especificado, atualiza a quantidade com o valor de entrada.
def reg_entrada(produto, qtd):
    for item in stock:
        if produto == item[0]:
            item[1] += qtd

# Função para cadastrar um novo produto no estoque.
# Verifica se o produto já está cadastrado, caso não esteja, adiciona o novo produto com a quantidade e preço inicial.
def cad_produto(produto, preco):
    for item in stock:
        if produto in item:
            print("Produto já cadastrado")
            break
    else:
        stock.append([produto, 0, preco, 0, 0])

# Função para registrar a saída de produtos do estoque.
# Verifica a quantidade disponível do produto e atualiza o estoque conforme o motivo (venda ou consumo).
def reg_saida(produto, qtd, motivo):
    for item in stock:
        if produto == item[0]:
            if qtd <= item[1]:
                item[1] -= qtd
                if motivo == "V":
                    item[3] += qtd
                else:
                    item[4] += qtd
                print("Saída registrada com sucesso!")
                break
            else:
                print("Quantidade insuficiente em estoque.")
                break
    else:
        print("Produto não encontrado.")

# Função para exibir o relatório de produtos no estoque.
# Limpa a tela, imprime um cabeçalho e lista os produtos com suas quantidades, preços, vendas e consumo.
def exibir_rel():
    os.system("clear")

    print("{:<20} | {:<15} | {:<20} | {:<15} | {:<15}".format("Produto", "Quantidade", "Preço", "Venda", "Consumo"))
    print("-" * 90)

    for item in stock:
        print("{:<20} | {:<15} | {:<20} | {:<15} | {:<15}".format(item[0].upper(), item[1], fmt_moeda(item[2]), item[3], item[4]))
    input("Pressione enter para continuar")


    with open("relatorio.txt", "w") as arquivo:
        arquivo.write("{:<20} | {:<15} | {:<20} | {:<15} | {:<15}".format("Produto", "Quantidade", "Preço", "Venda", "Consumo\n"))
        arquivo.write(f"{'-'*90}\n")

        for item in stock:
            arquivo.write("{:<20} | {:<15} | {:<20} | {:<15} | {:<15}\n".format(item[0].upper(), item[1], fmt_moeda(item[2]), item[3], item[4]))
def programa():
    while True:
        opcao = input(
            "\n- Cadastrar produto (0):\n"
            "- Controle de entrada de produto (1):\n"
            "- Controle de saída (2):\n"
            "- Exibir relatório (3):\n"
            "- Sair (4):\n"
            "- Digite sua opção: "
        )
        os.system('clear')
        # Informações de login fixas (para testes)
        user_name = "Diretor"
        user_pass = "diretor123"
        # Opção para sair do sistema
        if opcao == "4":
            print("Ok, Saindo...")
            time.sleep(2)
            print("Você saiu.")
            break
        # Opção para cadastrar um novo produto
        elif opcao == "0":
            if login("estoquista"):
                print("Acesso permitido")
                produto = input("Digite o nome do produto: ")
                preco = float(input("Digite o preço do produto: "))
                cad_produto(produto, preco)
            else:
                print("Acesso negado")
        # Opção para registrar entrada de produtos
        elif opcao == "1":
            if login("comprador"):
                print("Acesso permitido")
                produto = input("Digite o nome do produto: ")
                qtd = int(input("Digite a quantidade: "))
                reg_entrada(produto, qtd)
            else:
                print("Acesso negado")
        # Opção para registrar saída de produtos
        elif opcao == "2":
            if login("vendedor"):
                print("Acesso permitido")
                produto = input("Digite o nome do produto: ")
                qtd = int(input("Digite a quantidade: "))
                motivo = input("Digite (c) para consumo ou (v) para venda: ").upper()
                reg_saida(produto, qtd, motivo)
            else:
                print("Acesso negado")
        # Opção para exibir o relatório do estoque
        elif opcao == "3":
            if login("gerente"):
                print(f"Acesso liberado, {user_name}")
                exibir_rel()
            else:
                print("Acesso negado")
    # Caso a opção seja inválida
    else:
        print("A opção é inválida.")
        input("Pressione enter para continuar...")
        os.system("clear")
# Dados iniciais do estoque industrial
# Cada produto no estoque possui quantidade inicial, preço, quantidade vendida e quantidade consumida.
stock = []
with open("relatorio.txt", "r") as arquivo:
    # Ignorar as duas primeiras linhas
    next(arquivo)
    next(arquivo)

    # Iterar sobre as linhas restantes do arquivo
    for linha in arquivo:
        # Dividir a linha em elementos usando o separador "|"
        elementos = linha.strip().split("|")
        
        # Verificar se a linha tem o número esperado de elementos
        if len(elementos) == 5:
            # Remover espaços em branco ao redor de cada elemento e converter valores apropriados
            nome_produto = elementos[0].strip()
            quantidade = int(elementos[1].strip())
            preco = str(elementos[2].strip())
            vendas = int(elementos[3].strip())
            consumo = int(elementos[4].strip())

            # Adicionar os elementos a uma lista
            stock.append([nome_produto, quantidade, preco, vendas, consumo])
        else:
            # Se a linha não tiver o número esperado de elementos, imprimir um aviso
            print("A linha não tem o número esperado de elementos:", linha)

# Dados dos funcionários divididos por cargo.
# Cada funcionário possui nome, senha e telefone.
users = {
    "estoquista": [
        ["Carlos Silva",    "estoq123", "11987654321"],
        ["Mariana Santos",  "estoq456", "11998765432"],
        ["Rafael Costa",    "estoq789", "11912345678"],
        ["Laura Almeida",   "estoq101", "11987654333"],
        ["Diretor",         "diretor123", "11987654320"]
    ],
    "comprador": [
        ["João Pereira",    "compr123", "11976543210"],
        ["Ana Oliveira",    "compr456", "11987654322"],
        ["Paulo Souza",     "compr789", "11965432109"],
        ["Beatriz Silva",   "compr101", "11954321098"],
        ["Diretor",         "diretor123", "11987654320"]
    ],
    "vendedor": [
        ["Bruno Costa",     "vend123",  "11965432109"],
        ["Clara Ferreira",  "vend456",  "11976543211"],
        ["Diego Rocha",     "vend789",  "11943210987"],
        ["Juliana Lima",    "vend101",  "11932109876"],
        ["Diretor",         "diretor123", "11987654320"]
    ],
    "gerente": [
        ["Roberto Souza",   "ger123",   "11954321098"],
        ["Fernanda Lima",   "ger456",   "11965432122"],
        ["Marcelo Mendes",  "ger789",   "11998765433"],
        ["Patrícia Alves",  "ger101",   "11987654344"],
        ["Diretor",         "diretor123", "11987654320"]
    ]
}

# Loop principal para interação do usuário.
# Oferece opções para cadastrar produtos, controlar entrada e saída de produtos, exibir relatório ou sair do sistema.
programa()
