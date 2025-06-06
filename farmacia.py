import datetime
import sys
from typing import List, Dict, Tuple, Optional

# CLASSES DE DOMÍNIO

class Cliente:
    """
    Representa um cliente da farmácia.
    A busca se dará pelo CPF (string sem pontuação).

    Atributos:
        cpf (str): Identificador único do cliente (sem pontuação).
        nome (str): Nome completo do cliente.
        data_nascimento (datetime.date): Data de nascimento do cliente.
    """
    def __init__(self, cpf: str, nome: str, data_nascimento: datetime.date):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

    def idade(self) -> int:
        """Retorna a idade atual do cliente em anos completos."""
        hoje = datetime.date.today()
        anos = hoje.year - self.data_nascimento.year
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            anos -= 1
        return anos

    def __str__(self) -> str:
        return f"CPF: {self.cpf} | Nome: {self.nome} | Nasc.: {self.data_nascimento.isoformat()} | Idade: {self.idade()}"


class Laboratorio:
    """
    Representa um laboratório responsável por fabricar medicamentos.

    Atributos:
        nome (str): Nome do laboratório.
        endereco (str): Endereço completo.
        telefone (str): Telefone para contato.
        cidade (str): Cidade onde se localiza.
        estado (str): Estado (sigla).
    """
    def __init__(self, nome: str, endereco: str, telefone: str, cidade: str, estado: str):
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.cidade = cidade
        self.estado = estado

    def __str__(self) -> str:
        return f"{self.nome} | {self.endereco} | {self.telefone} | {self.cidade}-{self.estado}"


class Medicamento:
    """
    Classe base (abstrata) para qualquer medicamento.

    Atributos comuns:
        nome (str): Nome comercial do medicamento.
        composto_principal (str): Princípio ativo principal.
        laboratorio (Laboratorio): Instância de Laboratorio que fabrica.
        descricao (str): Descrição livre do medicamento.
        preco (float): Preço unitário do medicamento.
    """
    def __init__(self, nome: str, composto_principal: str, laboratorio: Laboratorio,
                 descricao: str, preco: float):
        self.nome = nome
        self.composto_principal = composto_principal
        self.laboratorio = laboratorio
        self.descricao = descricao
        self.preco = preco

    def __str__(self) -> str:
        return (f"{self.nome} | {self.composto_principal} | Lab: {self.laboratorio.nome} | "
                f"R$ {self.preco:.2f} | {self.descricao}")


class MedicamentoQuimioterapico(Medicamento):
    """
    Representa um medicamento quimioterápico.

    Atributos adicionais:
        necessita_receita (bool): Indica se exige apresentação de receita para venda.
    """
    def __init__(self, nome: str, composto_principal: str, laboratorio: Laboratorio,
                 descricao: str, preco: float, necessita_receita: bool):
        super().__init__(nome, composto_principal, laboratorio, descricao, preco)
        self.necessita_receita = necessita_receita

    def __str__(self) -> str:
        receitex = "Sim" if self.necessita_receita else "Não"
        return f"[Quimioterápico] {super().__str__()} | Receita: {receitex}"


class MedicamentoFitoterapico(Medicamento):
    """
    Representa um medicamento fitoterápico.
    (Não possui campo de receita.)

    Herda todos os atributos de Medicamento.
    """
    def __init__(self, nome: str, composto_principal: str, laboratorio: Laboratorio,
                 descricao: str, preco: float):
        super().__init__(nome, composto_principal, laboratorio, descricao, preco)

    def __str__(self) -> str:
        return f"[Fitoterápico] {super().__str__()}"


class Venda:
    """
    Representa uma venda realizada pela farmácia.

    Atributos:
        data_hora (datetime.datetime): Data e hora em que a venda foi efetuada.
        itens (List[Tuple[Medicamento, int]]): Lista de tuplas (medicamento, quantidade).
        cliente (Cliente): Cliente para quem a venda foi feita.
        valor_total (float): Valor final da venda (já com desconto aplicado, se houver).
    """
    def __init__(self, data_hora: datetime.datetime, itens: List[Tuple[Medicamento, int]],
                 cliente: Cliente, valor_total: float):
        self.data_hora = data_hora
        self.itens = itens
        self.cliente = cliente
        self.valor_total = valor_total

    def __str__(self) -> str:
        itens_str = "; ".join([f"{med.nome} x{qtde} (R$ {med.preco:.2f} cada)" for med, qtde in self.itens])
        return (f"Data/Hora: {self.data_hora.strftime('%Y-%m-%d %H:%M:%S')} | Cliente: {self.cliente.nome} | "
                f"Itens: [{itens_str}] | Total: R$ {self.valor_total:.2f}")

# REPOSITÓRIOS EM MEMÓRIA

clientes: Dict[str, Cliente] = {}
laboratorios: Dict[str, Laboratorio] = {}
medicamentos: Dict[str, Medicamento] = {}  # chave: nome do medicamento
vendas: List[Venda] = []

# Para estatísticas do dia:
#   - contador de vendas (para número de atendimentos)
#   - mapa de nome_medicamento -> (quantidade_vendida, valor_total)
estatisticas_itens_vendidos: Dict[str, Tuple[int, float]] = {}
total_quimio_vendido_qtde = 0
total_quimio_vendido_valor = 0.0
total_fito_vendido_qtde = 0
total_fito_vendido_valor = 0.0

# FUNÇÕES AUXILIARES DE CADASTRO E BUSCA

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

# FUNÇÃO DE VENDA

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
            qtde = int(input(f"Quantidade de '{med_sel.nome}': ").strip())
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

# FUNÇÕES DE RELATÓRIOS

def listar_clientes():
    """Exibe lista de clientes ordenados por nome (A-Z)."""
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
    print("\n--- Lista de Clientes (A-Z) ---")
    for cli in sorted(clientes.values(), key=lambda c: c.nome.lower()):
        print(cli)
    print()


def listar_todos_medicamentos():
    """Exibe todos os medicamentos (quimio e fito) em ordem alfabética por nome."""
    if not medicamentos:
        print("Nenhum medicamento cadastrado.")
        return
    print("\n--- Lista de Medicamentos (A-Z) ---")
    for med in sorted(medicamentos.values(), key=lambda m: m.nome.lower()):
        print(med)
    print()


def listar_medicamentos_por_tipo():
    """Pergunta ao usuário se deseja listar Quimioterápicos ou Fitoterápicos e exibe."""
    if not medicamentos:
        print("Nenhum medicamento cadastrado.")
        return
    print("Listar medicamentos por tipo:")
    print("1. Quimioterápicos")
    print("2. Fitoterápicos")
    escolha = input("Escolha (1/2): ").strip()
    if escolha == "1":
        lista_q = [m for m in medicamentos.values() if isinstance(m, MedicamentoQuimioterapico)]
        if not lista_q:
            print("Nenhum medicamento Quimioterápico cadastrado.")
        else:
            print("\n--- Medicamentos Quimioterápicos ---")
            for med in sorted(lista_q, key=lambda m: m.nome.lower()):
                print(med)
    elif escolha == "2":
        lista_f = [m for m in medicamentos.values() if isinstance(m, MedicamentoFitoterapico)]
        if not lista_f:
            print("Nenhum medicamento Fitoterápico cadastrado.")
        else:
            print("\n--- Medicamentos Fitoterápicos ---")
            for med in sorted(lista_f, key=lambda m: m.nome.lower()):
                print(med)
    else:
        print("Opção inválida.")
    print()


def gerar_relatorio_atendimentos_diarios():
    """
    Ao sair do programa, exibe estatísticas do dia de execução:
        - Remédio mais vendido (quantidade e valor total).
        - Quantidade de pessoas atendidas (número de vendas).
        - Número de remédios Quimioterápicos vendidos (qtde e valor).
        - Número de remédios Fitoterápicos vendidos (qtde e valor).
    """
    print("\n========== Relatório de Atendimento (Fim de Dia) ==========")
    num_vendas = len(vendas)
    print(f"Quantidade de pessoas atendidas (vendas realizadas): {num_vendas}")

    if estatisticas_itens_vendidos:
        # Encontrar remédio mais vendido em quantidade
        mais_vendido = max(estatisticas_itens_vendidos.items(), key=lambda x: x[1][0])
        nome_mv, (qt_mv, valor_mv) = mais_vendido
        print(f"Remédio mais vendido: {nome_mv} | Quantidade total vendida: {qt_mv} | Valor total: R$ {valor_mv:.2f}")
    else:
        print("Nenhum remédio vendido hoje.")

    print(f"\nTotal de remédios Quimioterápicos vendidos: {total_quimio_vendido_qtde} unidades | Valor total: R$ {total_quimio_vendido_valor:.2f}")
    print(f"Total de remédios Fitoterápicos vendidos: {total_fito_vendido_qtde} unidades | Valor total: R$ {total_fito_vendido_valor:.2f}")
    print("============================================================\n")

# MENU PRINCIPAL

def exibir_menu_principal():
    print("======== Farmácia E-Commerce ========")
    print("1. Cadastrar Cliente")
    print("2. Cadastrar Laboratório")
    print("3. Cadastrar Medicamento")
    print("4. Realizar Venda")
    print("5. Relatórios")
    print("6. Sair")
    print("=====================================")


def exibir_menu_relatorios():
    print("\n--- Menu de Relatórios ---")
    print("1. Listar Clientes (A-Z)")
    print("2. Listar Todos os Medicamentos (A-Z)")
    print("3. Listar Medicamentos por Tipo")
    print("4. Voltar ao Menu Principal")
    print("---------------------------")


def main():
    """
    Laço principal do programa: exibe menu, aguarda escolha do usuário e chama a função correspondente.
    Ao escolher “Sair” (opção 6), emite o relatório diário e finaliza.
    """
    while True:
        exibir_menu_principal()
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
            # Submenu de relatórios
            while True:
                exibir_menu_relatorios()
                sub = input("Escolha uma opção (1-4): ").strip()
                if sub == "1":
                    listar_clientes()
                elif sub == "2":
                    listar_todos_medicamentos()
                elif sub == "3":
                    listar_medicamentos_por_tipo()
                elif sub == "4":
                    break
                else:
                    print("Opção inválida. Tente novamente.\n")
        elif opcao == "6":
            # Ao sair, gerar relatório diário e encerrar
            gerar_relatorio_atendimentos_diarios()
            print("Programa encerrado. Até logo!")
            sys.exit(0)
        else:
            print("Opção inválida. Tente novamente.\n")


if __name__ == "__main__":
    main()
