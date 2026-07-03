# Sistema de Reserva de Salas de Estudo

Projeto desenvolvido para a disciplina de Verificação e Validação de Software.

## Objetivo

Implementar um sistema simples para gerenciamento de reservas de salas utilizando Python e validar seu funcionamento por meio de testes automatizados com Pytest.

## Funcionalidades

- Cadastro de alunos
- Consulta de salas disponíveis
- Reserva de salas
- Bloqueio de reservas duplicadas
- Consulta de histórico de reservas
- Tratamento de exceções específicas

## Estrutura

```
src/
    models.py
    exceptions.py
    sistema_reservas.py

tests/
    test_sistema_reservas.py

pytest.ini
conftest.py
```

## Tecnologias

- Python 3.13
- Pytest
- pytest-cov

## Instalação

Clone o repositório:

```bash
git clone <url>
```

Instale as dependências:

```bash
pip install pytest pytest-cov
```

## Executando os testes

```bash
pytest -v
```

## Gerando cobertura

```bash
pytest --cov=src --cov-report=term-missing
```

## Resultado

- 11 testes automatizados
- 11 testes aprovados
- Cobertura de código: 100%

## Organização

```
src/
    Lógica de negócio

tests/
    Testes automatizados

models.py
    Entidades

exceptions.py
    Exceções

sistema_reservas.py
    Regras de negócio
```

## Autora

Vivian Gomes de Brito
