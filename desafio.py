import textwrap

def menu():
    menu = """\n
    ============ Menu ============
    [d] Depositar
    [s] Sacar
    [e] Extrato

    [nc] Nova Conta
    [lc] Listar Contas
    [nu] Novo Usuário
    
    [q] Sair
    =>"""
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso.")
    else:
        print("Operação falhou. O valor informado é inválido.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou. Saldo insuficiente.")

    elif excedeu_limite:
        print("Operação falhou. Este valor de saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou. Quantidade de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso.")

    else:
        print("Operação falhou. O valor informado é inválido.")

def exibir_extrato(saldo, /, *, extrato):
    print(" Extrato bancário ".center(42, "="))
    print(f"Saldo: R$ {saldo:.2f}")
    print("Não foram realizadas movimentações" if not extrato else f"Histórico de Operações:\n{extrato}")
    print("="*42)

def criar_usuario(usuarios):
    cpf = input("Digite o CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Usuário já existente.")
        return
    
    nome = input("Digite o nome completo: ")
    data_nascimento = input("Digite a data de nascimento: ")
    endereco = input("Digite o endereço: ")

    usuarios.append({"nome": nome, "cpf": cpf, "data_nascimento": data_nascimento, "endereco": endereco})

    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Digite o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "cpf": cpf, "saldo": 0, "limite": 500, "extrato": "", "numero_saques": 0, "usuario": usuario}

    print("\nUsuário não encontrado. Conta não criada.")
    return None

def listar_contas(contas):
    for conta in contas:
        lista = f"""
                Agência:\t{conta['agencia']}
                Conta:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome'].upper()}
        """
        print("="*100)
        print(textwrap.dedent(lista))

def main():
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    LIMITE_SAQUES = 3

    while True:

        opcao = menu()

        if opcao == 'q':
            break
        
        elif opcao == 'd':
            valor = float(input("Digite o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 's':
            valor = float(input("Digite o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo, 
                valor=valor, 
                extrato=extrato, 
                limite=limite, 
                numero_saques=numero_saques, 
                limite_saques=LIMITE_SAQUES)

        elif opcao == 'e':
            exibir_extrato(saldo, extrato=extrato)
            
        elif opcao == 'nu':
            criar_usuario(usuarios)

        elif opcao == 'nc':
            numero_conta = len(contas) +1 #funciona pois não temos exclusão de contas
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == 'lc':
            listar_contas(contas)
            

        else:
            print("Opção inválida.")
            continue

main()