from .laboratorio import Laboratorio

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

