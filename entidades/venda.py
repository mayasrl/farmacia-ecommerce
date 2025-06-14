import datetime
from typing import List, Tuple
from .medicamento import Medicamento
from .cliente import Cliente

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

