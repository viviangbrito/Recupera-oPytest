"""
Testes automatizados do Sistema de Reserva de Salas de Estudo.

Cada função corresponde a um caso de teste do Plano de Testes Funcionais.
O identificador (TCxx) no docstring garante rastreabilidade entre o
plano de testes e o código automatizado.

Para executar:
    pytest -v

Para executar com relatório de cobertura:
    pytest --cov=src --cov-report=term-missing
"""
from datetime import date, time

import pytest

from src.models import Sala
from src.sistema_reservas import SistemaReservas
from src.exceptions import (
    AlunoJaCadastradoError,
    AlunoNaoEncontradoError,
    SalaNaoEncontradaError,
    HorarioOcupadoError,
)


@pytest.fixture
def sistema():
    """
    Fixture que cria uma instância limpa do SistemaReservas com duas
    salas pré-cadastradas. É recriada antes de cada teste, garantindo
    que um teste nunca interfere no estado de outro.
    """
    salas = [
        Sala(codigo="S01", nome="Sala de Estudo 1", capacidade=4),
        Sala(codigo="S02", nome="Sala de Estudo 2", capacidade=6),
    ]
    return SistemaReservas(salas=salas)


# ---------------------------------------------------------------------- #
# TC01 — RF01: Cadastro de aluno com sucesso
# ---------------------------------------------------------------------- #
def test_cadastrar_aluno_com_sucesso(sistema):
    """TC01: um aluno novo deve ser cadastrado com os dados corretos."""
    aluno = sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")

    assert aluno.matricula == "2025001"
    assert aluno.nome == "Vívian Silva"
    assert "2025001" in sistema._alunos


# ---------------------------------------------------------------------- #
# TC02 — RF01: Cadastro com matrícula duplicada deve ser rejeitado
# ---------------------------------------------------------------------- #
def test_cadastrar_aluno_duplicado_lanca_erro(sistema):
    """TC02: a mesma matrícula não pode ser cadastrada duas vezes."""
    sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")

    with pytest.raises(AlunoJaCadastradoError):
        sistema.cadastrar_aluno("2025001", "Outro Nome", "outro@email.com")


# ---------------------------------------------------------------------- #
# TC03 — RF02: Consulta de salas disponíveis sem nenhuma reserva
# ---------------------------------------------------------------------- #
def test_consultar_salas_disponiveis_sem_reservas(sistema):
    """TC03: sem reservas no horário, todas as salas aparecem como livres."""
    disponiveis = sistema.consultar_salas_disponiveis(date(2026, 7, 1), time(14, 0))
    codigos = {s.codigo for s in disponiveis}

    assert codigos == {"S01", "S02"}


# ---------------------------------------------------------------------- #
# TC04 — RF02: Sala reservada não deve aparecer como disponível
# ---------------------------------------------------------------------- #
def test_sala_reservada_nao_aparece_como_disponivel(sistema):
    """TC04: sala reservada some da lista naquele horário, mas continua
    livre em outros horários."""
    sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")
    sistema.realizar_reserva("2025001", "S01", date(2026, 7, 1), time(14, 0))

    disponiveis_mesmo_horario = sistema.consultar_salas_disponiveis(
        date(2026, 7, 1), time(14, 0)
    )
    disponiveis_outro_horario = sistema.consultar_salas_disponiveis(
        date(2026, 7, 1), time(16, 0)
    )

    assert {s.codigo for s in disponiveis_mesmo_horario} == {"S02"}
    assert {s.codigo for s in disponiveis_outro_horario} == {"S01", "S02"}


# ---------------------------------------------------------------------- #
# TC05 — RF03: Realizar reserva com sucesso
# ---------------------------------------------------------------------- #
def test_realizar_reserva_com_sucesso(sistema):
    """TC05: aluno cadastrado consegue reservar uma sala livre."""
    sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")
    reserva = sistema.realizar_reserva("2025001", "S01", date(2026, 7, 1), time(14, 0))

    assert reserva.codigo_sala == "S01"
    assert reserva.matricula_aluno == "2025001"
    assert reserva.id_reserva == 1


# ---------------------------------------------------------------------- #
# TC06 — RF04: Impedir reserva em horário já ocupado
# ---------------------------------------------------------------------- #
def test_reserva_horario_ocupado_lanca_erro(sistema):
    """TC06: segunda tentativa de reservar a mesma sala no mesmo horário
    deve ser rejeitada (RF04)."""
    sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")
    sistema.cadastrar_aluno("2025002", "Outro Aluno", "outro@email.com")
    sistema.realizar_reserva("2025001", "S01", date(2026, 7, 1), time(14, 0))

    with pytest.raises(HorarioOcupadoError):
        sistema.realizar_reserva("2025002", "S01", date(2026, 7, 1), time(14, 0))


# ---------------------------------------------------------------------- #
# TC07 — RF05: Consultar histórico de reservas
# ---------------------------------------------------------------------- #
def test_consultar_historico_de_reservas(sistema):
    """TC07: histórico retorna exatamente as reservas do aluno consultado,
    na ordem em que foram criadas."""
    sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")
    sistema.realizar_reserva("2025001", "S01", date(2026, 7, 1), time(14, 0))
    sistema.realizar_reserva("2025001", "S02", date(2026, 7, 2), time(10, 0))

    historico = sistema.consultar_historico("2025001")

    assert len(historico) == 2
    assert historico[0].codigo_sala == "S01"
    assert historico[1].codigo_sala == "S02"


# ---------------------------------------------------------------------- #
# TC08 — Integridade RF01+RF03: aluno não cadastrado não pode reservar
# ---------------------------------------------------------------------- #
def test_reserva_aluno_nao_cadastrado_lanca_erro(sistema):
    """TC08: matrícula não cadastrada não pode ser usada para reservas."""
    with pytest.raises(AlunoNaoEncontradoError):
        sistema.realizar_reserva("9999999", "S01", date(2026, 7, 1), time(14, 0))


# ---------------------------------------------------------------------- #
# TC09 — Integridade: reserva em sala inexistente deve falhar
# ---------------------------------------------------------------------- #
def test_reserva_sala_inexistente_lanca_erro(sistema):
    """TC09: código de sala inexistente deve ser rejeitado."""
    sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")

    with pytest.raises(SalaNaoEncontradaError):
        sistema.realizar_reserva("2025001", "S99", date(2026, 7, 1), time(14, 0))


# ---------------------------------------------------------------------- #
# TC10 — RNF03: tempo de resposta deve ser inferior a 3 segundos
# ---------------------------------------------------------------------- #
def test_tempo_resposta_reserva_abaixo_de_3_segundos(sistema):
    """TC10: valida o requisito não funcional RNF03 medindo o tempo de
    execução de realizar_reserva."""
    import time as time_module

    sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")

    inicio = time_module.perf_counter()
    sistema.realizar_reserva("2025001", "S01", date(2026, 7, 1), time(14, 0))
    duracao = time_module.perf_counter() - inicio

    assert duracao < 3.0


# ---------------------------------------------------------------------- #
# TC11 — RF05: consultar histórico de aluno não cadastrado deve falhar
# ---------------------------------------------------------------------- #
def test_consultar_historico_aluno_nao_cadastrado_lanca_erro(sistema):
    """TC11: consultar histórico com matrícula inválida deve lançar erro.
    Este teste cobre o único branch que faltava, elevando a cobertura
    de 97,8% para 100%."""
    with pytest.raises(AlunoNaoEncontradoError):
        sistema.consultar_historico("9999999")
