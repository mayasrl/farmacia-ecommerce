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

