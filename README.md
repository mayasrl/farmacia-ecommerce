# 💊 Farmácia E-Commerce

Um **sistema de console em Python orientado a objetos** para gerenciar cadastros, vendas e relatórios de uma farmácia online.  

---

## 🧐 Visão Geral

- **Python 3.6+**: apenas módulos nativos (`datetime`, `sys`, `typing`).  
- **Arquitetura OOP**: classes `Cliente`, `Laboratorio`, `MedicamentoQuimioterápico`, `MedicamentoFitoterápico` e `Venda`.  
- **Dados em memória**: utiliza dicionários e listas, sem banco de dados ou arquivos externos.  
- **Interface via console**: menu interativo para cadastro, venda e geração de relatórios.  
- **Saída formatada**: relatórios ao final da sessão com estatísticas de vendas.

---

## 📁 Estrutura do Projeto

- **`farmacia.py`** — Script principal com toda a lógica orientada a objetos.  
- **`README.md`** — Documentação do projeto (você está aqui!).

---

## 🚀 Funcionalidades

1. **Cadastro de Clientes**  
   - CPF (somente números), nome e data de nascimento;  
   - Cálculo automático de idade para desconto de idoso (> 65 anos).

2. **Cadastro de Laboratórios**  
   - Nome, endereço, telefone, cidade e estado.

3. **Cadastro de Medicamentos**  
   - **Quimioterápicos** (flag “necessita receita”);  
   - **Fitoterápicos**;  
   - Princípio ativo, descrição e preço unitário.

4. **Realizar Venda**  
   - Busca por nome, laboratório ou descrição parcial;  
   - Adição de múltiplos itens e quantidades;  
   - Alerta automático para quimioterápicos controlados;  
   - Aplicação do maior desconto (20% idoso ou 10% compras ≥ R$ 150);  
   - Confirmação e registro da venda em memória.

5. **Relatórios**  
   - Listar clientes (A → Z);  
   - Listar todos os medicamentos (A → Z);  
   - Filtrar por tipo (Quimioterápico / Fitoterápico);  
   - Relatório de vendas ao sair, com:  
     - Total de atendimentos;  
     - Remédio mais vendido (quantidade & valor);  
     - Totais de quimioterápicos e fitoterápicos vendidos.

---

## 📷 Exemplo de Saída

```console
$ python farmacia.py
Iniciando sistema de Farmácia E-Commerce…

======== Farmácia E-Commerce ========
1. Cadastrar Cliente
2. Cadastrar Laboratório
3. Cadastrar Medicamento
4. Realizar Venda
5. Relatórios
6. Sair
=====================================
Escolha uma opção (1-6): 4

— Realizar Venda —
CPF: 12345678901
Itens:
  1. Paracetamol x2 (R$ 5.00 cada)
  2. Chá de Camomila x3 (R$ 3.00 cada)
Subtotal: R$ 19.00
Nenhum desconto aplicado.
Valor final: R$ 19.00
Venda confirmada! 🛒

Escolha uma opção (1-6): 6

========== Relatório de Vendas (Sessão) ==========
Clientes atendidos: 1

Remédio mais vendido: Paracetamol  
Quantidade total vendida: 2 unidades  
Valor total: R$ 10.00

Total de Quimioterápicos vendidos: 2 unidades | Valor total: R$ 10.00  
Total de Fitoterápicos vendidos: 3 unidades | Valor total: R$ 9.00  
==================================================
```

---

<p align="center"> Desenvolvido durante o curso <strong>Academia Globotech</strong> com 💛 por <strong>@mayasrl</strong> da Ada em parceria com a Globo. </p> 
