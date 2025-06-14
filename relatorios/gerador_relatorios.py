from entidades.cliente import Cliente
from entidades.medicamento import Medicamento, MedicamentoQuimioterapico, MedicamentoFitoterapico
from data import clientes, medicamentos, vendas, estatisticas_itens_vendidos, total_quimio_vendido_qtde, total_quimio_vendido_valor, total_fito_vendido_qtde, total_fito_vendido_valor

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
    tipo = input("Listar medicamentos ([Q]uimio / [F]ito): ").strip().upper()
    if tipo not in ("Q", "F"):
        print("Tipo inválido.")
        return

    print("\n--- Lista de Medicamentos {}".format("Quimioterápicos" if tipo == "Q" else "Fitoterápicos"))
    for med in sorted(medicamentos.values(), key=lambda m: m.nome.lower()):
        if (tipo == "Q" and isinstance(med, MedicamentoQuimioterapico)) or \
           (tipo == "F" and isinstance(med, MedicamentoFitoterapico)):
            print(med)
    print()


def exibir_estatisticas_dia():
    """
    Exibe as estatísticas de vendas do dia (sessão atual).
    """
    print("\n========== Relatório de Vendas (Sessão) ==========")
    print(f"Clientes atendidos: {len(vendas)}")

    if estatisticas_itens_vendidos:
        # Remédio mais vendido
        mais_vendido_nome = max(estatisticas_itens_vendidos, key=lambda k: estatisticas_itens_vendidos[k][0])
        qtde_mais_vendido, valor_mais_vendido = estatisticas_itens_vendidos[mais_vendido_nome]
        print(f"Remédio mais vendido: {mais_vendido_nome}")
        print(f"Quantidade total vendida: {qtde_mais_vendido} unidades")
        print(f"Valor total: R$ {valor_mais_vendido:.2f}")
    else:
        print("Nenhum medicamento vendido ainda.")

    print(f"Total de Quimioterápicos vendidos: {total_quimio_vendido_qtde} unidades | Valor total: R$ {total_quimio_vendido_valor:.2f}")
    print(f"Total de Fitoterápicos vendidos: {total_fito_vendido_qtde} unidades | Valor total: R$ {total_fito_vendido_valor:.2f}")
    print("==================================================\n")


