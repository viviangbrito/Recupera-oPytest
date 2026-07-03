"""
Exceções customizadas do Sistema de Reserva de Salas de Estudo.

Usar exceções específicas facilita a leitura do código e a escrita
de testes automatizados, pois cada caso de erro previsto nos
requisitos tem um tipo próprio verificado com pytest.raises(...).
"""


class AlunoJaCadastradoError(Exception):
    """Levantada ao tentar cadastrar uma matrícula que já existe (RF01)."""


class AlunoNaoEncontradoError(Exception):
    """Levantada quando a matrícula informada não corresponde a nenhum aluno."""


class SalaNaoEncontradaError(Exception):
    """Levantada quando o código de sala informado não existe no sistema."""


class HorarioOcupadoError(Exception):
    """Levantada ao tentar reservar uma sala em horário já ocupado (RF04)."""
