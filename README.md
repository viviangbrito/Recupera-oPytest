# Sistema de Reserva de Salas de Estudo

Projeto desenvolvido para a disciplina de Verificação e Validação de Software.

## Objetivo

Implementar um sistema simples para gerenciamento de reservas de salas utilizando Python e validar seu funcionamento por meio de testes automatizados com Pytest.

## Funcionalidades

- Cadastro de alunos
- Consulta de salas disponíveis
- Reserva de salas
- Bloqueio de reservas duplicadas
- Consulta do histórico de reservas
- Tratamento de exceções específicas

## Estrutura

```
src/
    models.py
    exceptions.py
    sistema_reservas.py

tests/
    test_sistema_reservas.py

demo.py
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
git clone https://github.com/viviangbrito/Recupera-oPytest.git
```

Entre na pasta do projeto:

```bash
cd Recupera-oPytest
```

Instale as dependências:

```bash
pip install pytest pytest-cov
```

## Executando uma demonstração

O arquivo `demo.py` executa uma demonstração das principais funcionalidades do sistema, incluindo:

- Cadastro de aluno
- Consulta de salas disponíveis
- Realização de reserva
- Consulta das salas após a reserva
- Consulta do histórico de reservas

Execute com:

```bash
python demo.py
```

## Executando os testes automatizados

```bash
python -m pytest -v
```

## Gerando o relatório de cobertura

```bash
python -m pytest --cov=src --cov-report=term-missing
```

## Resultado esperado

- 11 testes automatizados
- 11 testes aprovados
- Cobertura de código: 100%

## Organização do Projeto

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
