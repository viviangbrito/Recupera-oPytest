from datetime import date, time
from src.models import Sala
from src.sistema_reservas import SistemaReservas

salas = [
    Sala("S01", "Sala de Estudo 1", 4),
    Sala("S02", "Sala de Estudo 2", 6)
]

sistema = SistemaReservas(salas)

print("Cadastro de aluno")
print(sistema.cadastrar_aluno(
    "2025001",
    "Vivian Gomes de Brito",
    "vivian@email.com"
))

print("\nSalas disponíveis")
print(sistema.consultar_salas_disponiveis(
    date(2026, 7, 1),
    time(14, 0)
))

print("\nReserva")
print(sistema.realizar_reserva(
    "2025001",
    "S01",
    date(2026, 7, 1),
    time(14, 0)
))

print("\nSalas disponíveis após a reserva")
print(sistema.consultar_salas_disponiveis(
    date(2026, 7, 1),
    time(14, 0)
))

print("\nHistórico")
print(sistema.consultar_historico("2025001"))