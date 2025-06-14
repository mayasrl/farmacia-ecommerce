from typing import List, Dict, Tuple
from entidades.cliente import Cliente
from entidades.laboratorio import Laboratorio
from entidades.medicamento import Medicamento
from entidades.venda import Venda

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

