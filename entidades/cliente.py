import datetime

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

