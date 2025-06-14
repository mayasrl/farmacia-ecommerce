import datetime
import sys
from typing import List, Dict, Tuple, Optional

from entidades.cliente import Cliente
from entidades.laboratorio import Laboratorio
from entidades.medicamento import Medicamento, MedicamentoQuimioterapico, MedicamentoFitoterapico
from entidades.venda import Venda
from data import clientes, laboratorios, medicamentos, vendas, estatisticas_itens_vendidos, total_quimio_vendido_qtde, total_quimio_vendido_valor, total_fito_vendido_qtde, total_fito_vendido_valor

def cadastrar_cliente():
    """Solicita dados e cadastra um cliente novo, indexando por CPF."""
    cpf = input("Digite o CPF (somente números): ").strip()
    if cpf in clientes:
        print("Cliente com este CPF já existe!")
        return
    nome = input("Digite o nome completo: ").strip()
    data_str = input("Digite a data de nascimento (YYYY-MM-DD): ").strip()
    try:
        data_nascimento = datetime.datetime.strptime(data_str, "%Y-%m-%d").date()
    except ValueError:
        print("Formato de data inválido. Cadastro cancelado.")
        return
    novo = Cliente(cpf, nome, data_nascimento)
    clientes[cpf] = novo
    print("Cliente cadastrado com sucesso!\n")


def cadastrar_laboratorio():
    """Solicita dados e cadastra um laboratório novo."""
    nome = input("Digite o nome do laboratório: ").strip()
    if nome in laboratorios:
        print("Laboratório com este nome já existe!")
        return
    endereco = input("Digite o endereço completo: ").strip()
    telefone = input("Digite o telefone para contato: ").strip()
    cidade = input("Digite a cidade: ").strip()
    estado = input("Digite o estado (sigla): ").strip().upper()
    lab = Laboratorio(nome, endereco, telefone, cidade, estado)
    laboratorios[nome] = lab
    print("Laboratório cadastrado com sucesso!\n")


def escolher_laboratorio() -> Optional[Laboratorio]:
    """Exibe labs cadastrados e retorna a instância escolhida, ou None se não houver."""
    if not laboratorios:
        print("Nenhum laboratório cadastrado. Cadastre um antes de criar medicamentos.")
        return None
    print("Laboratórios disponíveis:")
    for idx, lab in enumerate(laboratorios.values(), start=1):
        print(f"{idx}. {lab.nome} ({lab.cidade}-{lab.estado})")
    try:
        escolha = int(input("Escolha o número do laboratório: ").strip())
        lista_labs = list(laboratorios.values())
        return lista_labs[escolha - 1]
    except (ValueError, IndexError):
        print("Escolha inválida.")
        return None


def cadastrar_medicamento():
    """
    Pergunta se o medicamento é Quimioterápico ou Fitoterápico,
    coleta os dados, e insere no dicionário `medicamentos` indexado pelo nome.
    """
    tipo = input("Tipo de medicamento ([Q]uimio / [F]ito): ").strip().upper()
    if tipo not in ("Q", "F"):
        print("Tipo inválido.")
        return

    nome = input("Digite o nome comercial do medicamento: ").strip()
    if nome in medicamentos:
        print("Medicamento com este nome já existe!")
        return

    composto = input("Digite o princípio ativo principal: ").strip()
    lab = escolher_laboratorio()
    if lab is None:
        return
    descricao = input("Digite uma breve descrição: ").strip()
    try:
        preco = float(input("Digite o preço unitário (use ponto decimal): ").strip())
        if preco < 0:
            raise ValueError
    except ValueError:
        print("Preço inválido. Cadastro cancelado.")
        return

    if tipo == "Q":
        rec = input("Necessita receita? ([S]im/[N]ão): ").strip().upper()
        necessita_receita = rec == "S"
        mq = MedicamentoQuimioterapico(nome, composto, lab, descricao, preco, necessita_receita)
        medicamentos[nome] = mq
    else:
        mf = MedicamentoFitoterapico(nome, composto, lab, descricao, preco)
        medicamentos[nome] = mf

    print("Medicamento cadastrado com sucesso!\n")


def buscar_cliente_por_cpf(cpf: str) -> Optional[Cliente]:
    """Retorna o Cliente se existir, senão None."""
    return clientes.get(cpf)


def menu_buscar_medicamentos() -> List[Medicamento]:
    """
    Permite buscar por nome exato, por fabricante (nome do laboratório) ou
    por descrição parcial dentro do tipo de medicamento.
    Retorna lista de instâncias encontradas.
    """
    if not medicamentos:
        print("Nenhum medicamento cadastrado.")
        return []

    print("Buscar medicamentos por:")
    print("1. Nome exato")
    print("2. Nome do laboratório")
    print("3. Texto parcial na descrição")
    escolha = input("Escolha (1/2/3): ").strip()

    encontrados: List[Medicamento] = []
    if escolha == "1":
        termo = input("Digite o nome exato do medicamento: ").strip()
        med = medicamentos.get(termo)
        if med:
            encontrados.append(med)
    elif escolha == "2":
        termo = input("Digite o nome do laboratório: ").strip().lower()
        for med in medicamentos.values():
            if med.laboratorio.nome.lower() == termo:
                encontrados.append(med)
    elif escolha == "3":
        termo = input("Digite texto parcial para buscar na descrição: ").strip().lower()
        for med in medicamentos.values():
            if termo in med.descricao.lower():
                encontrados.append(med)
    else:
        print("Opção inválida.")

    if not encontrados:
        print("Nenhum medicamento encontrado com os critérios informados.")
    return encontrados


def realizar_venda():
    """
    Controla todo o fluxo de uma venda:
      - Verifica cliente cadastrado por CPF;
      - Permite adicionar múltiplos itens (medicamento + quantidade);
      - Aplica descontos (idoso > 65 anos ou compras acima de R$150);
      - Gera alerta se houver medicamento quimioterápico controlado (necessita_receita=True);
      - Armazena a Venda e atualiza estatísticas diárias.
    """
    global total_quimio_vendido_qtde, total_quimio_vendido_valor
    global total_fito_vendido_qtde, total_fito_vendido_valor

    cpf = input("CPF do cliente para a venda (somente números): ").strip()
    cliente = buscar_cliente_por_cpf(cpf)
    if cliente is None:
        print("Cliente não cadastrado. Operação cancelada.\n")
        return

    itens_venda: List[Tuple[Medicamento, int]] = []
    subtotal = 0.0
    tem_quimio_controlado = False
    nomes_quimio_controlados: List[str] = []

    while True:
        print("\n--- Adicionar item ---")
        encontrados = menu_buscar_medicamentos()
        if not encontrados:
            # possibilidade de encerrar busca sem achar nada
            resp = input("Deseja tentar outra busca? ([S]im/[N]ão): ").strip().upper()
            if resp != "S":
                break
            else:
                continue

        # se houve mais de um resultado, perguntar qual deseja
        if len(encontrados) > 1:
            print("Vários medicamentos encontrados:")
            for idx, m in enumerate(encontrados, start=1):
                print(f"{idx}. {m}")
            try:
                escolha = int(input("Escolha o número do medicamento desejado: ").strip())
                med_sel = encontrados[escolha - 1]
            except (ValueError, IndexError):
                print("Escolha inválida. Voltando ao menu de adicionar item.")
                continue
        else:
            med_sel = encontrados[0]

        try:
            qtde = int(input(f"Quantidade de \'{med_sel.nome}\' ").strip())
            if qtde <= 0:
                raise ValueError
        except ValueError:
            print("Quantidade inválida. Item não adicionado.")
            continue

        itens_venda.append((med_sel, qtde))
        subtotal += med_sel.preco * qtde

        # Se for Quimioterápico controlado, marca alerta
        if isinstance(med_sel, MedicamentoQuimioterapico) and med_sel.necessita_receita:
            tem_quimio_controlado = True
            nomes_quimio_controlados.append(med_sel.nome)

        resp = input("Deseja adicionar outro medicamento? ([S]im/[N]ão): ").strip().upper()
        if resp != "S":
            break

    if not itens_venda:
        print("Nenhum item adicionado. Venda cancelada.\n")
        return

    # Alerta para checar receita, se aplicável
    if tem_quimio_controlado:
        nomes_str = ", ".join(nomes_quimio_controlados)
        print(f"\n*** ATENÇÃO: Verifique a receita para o(s) medicamento(s): {nomes_str} ***\n")

    # Cálculo de descontos
    desconto_idoso = 0.0
    desconto_valor = 0.0
    if cliente.idade() > 65:
        desconto_idoso = 0.20  # 20%
    if subtotal > 150.0:
        desconto_valor = 0.10  # 10%

    desconto_aplicado = max(desconto_idoso, desconto_valor)
    valor_desconto = subtotal * desconto_aplicado
    total_final = subtotal - valor_desconto

    print(f"Subtotal: R$ {subtotal:.2f}")
    if desconto_aplicado > 0:
        tipo_desc = "20% (Idoso)" if desconto_aplicado == 0.20 else "10% (>= R$150)"
        print(f"Desconto aplicado: {tipo_desc} => R$ {valor_desconto:.2f}")
    else:
        print("Nenhum desconto aplicado.")
    print(f"Valor final da venda: R$ {total_final:.2f}\n")

    confirma = input("Confirmar venda? ([S]im/[N]ão): ").strip().upper()
    if confirma != "S":
        print("Venda não confirmada.\n")
        return

    # Criar instância de Venda
    venda = Venda(datetime.datetime.now(), itens_venda, cliente, total_final)
    vendas.append(venda)

    # Atualizar estatísticas
    for med, qt in itens_venda:
        # Estatísticas gerais de itens vendidos
        nome_med = med.nome
        qtd_antiga, valor_antigo = estatisticas_itens_vendidos.get(nome_med, (0, 0.0))
        estatisticas_itens_vendidos[nome_med] = (qtd_antiga + qt, valor_antigo + med.preco * qt)

        # Estatísticas por tipo (Quimioterápico ou Fitoterápico)
        if isinstance(med, MedicamentoQuimioterapico):
            total_quimio_vendido_qtde += qt
            total_quimio_vendido_valor += med.preco * qt
        elif isinstance(med, MedicamentoFitoterapico):
            total_fito_vendido_qtde += qt
            total_fito_vendido_valor += med.preco * qt

    print("Venda registrada com sucesso!\n")



