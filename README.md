# API Sondas - Exploração de Marte

Sistema de controle e gerenciamento de sondas espaciais para exploração de planalto marciano através de API REST.

## 📑 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Requisitos do Sistema](#requisitos-do-sistema)
- [Arquitetura](#arquitetura)
- [Instalação e Execução](#instalação-e-execução)
- [Documentação da API](#documentação-da-api)
- [Testes](#testes)

## Sobre o Projeto

A API Sondas é uma aplicação REST desenvolvida para controlar o movimento de sondas robóticas em missão de exploração em Marte. O sistema permite lançar sondas, definir limites de exploração e controlar movimentos através de comandos sequenciais, garantindo que as sondas permaneçam dentro dos limites estabelecidos.

### Funcionalidades Principais

- Criação de sondas com posicionamento inicial e definição de malha de exploração
- Controle de movimento através de comandos de rotação (L/R) e translação (M)
- Consulta de posição e estado atual de todas as sondas ativas
- Validação automática de movimentos e limites de área
- Persistência de dados em formato JSON

## Requisitos do Sistema

### Dependências Obrigatórias

| Componente | Versão Mínima | Versão Recomendada | Notas |
|------------|---------------|-------------------|-------|
| Python | 3.12.0 | 3.12.8 | Requer recursos do Python 3.12+ |
| Poetry | 2.0.0 | 2.1.3 | Gerenciador de dependências |

### Dependências Opcionais (Docker)

| Componente | Versão Mínima | Notas |
|------------|---------------|-------|
| Docker | 20.10.0 | Para execução containerizada |
| Docker Compose | 2.0.0 | Orquestração de containers |

### Stack

```
FastAPI 0.104+      # Framework web assíncrono
├── Uvicorn         # Servidor ASGI
├── Pydantic 2.0+   # Validação de dados
└── Python 3.12.8   # Runtime

Pytest 7.4+         # Framework de testes
└── pytest-cov      # Relatórios de cobertura
```

## Arquitetura

### Estrutura de Diretórios

```
probe-api/
├── src/
│   ├── api/
│   │   ├── controller/
│   │   │   ├── __init__.py
│   │   │   └── probe_controller.py      # Endpoints REST
│   │   └── schemas/
│   │       ├── requests/
│   │       │   ├── CreateEnvironment.py # Schema de criação
│   │       │   └── MoveProbe.py         # Schema de movimento
│   │       └── __init__.py
│   ├── service/
│   │   ├── __init__.py
│   │   └── probe_service.py             # Lógica de negócio
│   ├── data/
│   │   ├── __init__.py
│   │   └── probe_repository.py          # Camada de persistência
│   └── server.py                        # Configuração FastAPI
├── tests/
│   ├── conftest.py                      # Fixtures de teste
│   ├── test_probe_service.py
│   ├── test_probe_repository.py
│   └── test_probe_validators.py
├── db/
│   └── probes.json                      # Armazenamento (auto-criado)
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml                       # Dependências Poetry
├── main.py                              # Entry point
└── README.md
```

## Instalação e Execução

### Método 1: Docker

**Pré-requisitos:** Docker e Docker Compose instalados

```bash
# Clone o repositório
git clone <repository-url>
cd probe-api

# Inicie o container
docker-compose up --build 

# Verificar status
docker-compose ps

# Visualizar logs
docker-compose logs -f
```

**Acesso à aplicação:**
- API Base: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs
- Documentação ReDoc: http://localhost:8000/redoc

### Método 2: Ambiente Local

**Pré-requisitos:** Python 3.12.8+ e Poetry 2.1.3+

#### Instalação do Poetry

```bash
# Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -

# Verificar instalação
poetry --version
```

#### Setup do Projeto

```bash
# Clone o repositório
git clone <repository-url>
cd probe-api

# Configure o Poetry para criar virtualenv no diretório do projeto
poetry config virtualenvs.in-project true

# Instale as dependências
poetry install

# Ative o ambiente virtual
poetry shell

# Execute a aplicação
python main.py
```

#### Execução em Modo Desenvolvimento

```bash
# Com hot-reload habilitado
poetry run uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload

# Em modo debug
poetry run uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

## Documentação da API

### Endpoint: Criar Sonda e Ambiente

Inicializa uma nova sonda na posição (0,0) e define os limites da malha de exploração.

**Request:**
```http
POST /create-environment
Content-Type: application/json

{
    "x": 5,
    "y": 5,
    "direction": "NORTH"
}
```

**Parâmetros:**

| Campo | Tipo | Requerido | Descrição | Valores Válidos |
|-------|------|-----------|-----------|-----------------|
| x | int | Sim | Coordenada X do limite superior direito | ≥ 0 |
| y | int | Sim | Coordenada Y do limite superior direito | ≥ 0 |
| direction | string | Sim | Direção inicial da sonda | NORTH, SOUTH, EAST, WEST |

**Response:** `200 OK`
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "x": 0,
    "y": 0,
    "direction": "NORTH"
}
```

### Endpoint: Mover Sonda

Executa uma sequência de comandos de movimento para uma sonda específica.

**Request:**
```http
PUT /move-probe/{probe_id}
Content-Type: application/json

{
    "instruction": "LMLMLMLMM"
}
```

**Comandos Disponíveis:**

| Comando | Ação | Efeito |
|---------|------|--------|
| L | Rotate Left | Rotaciona 90° à esquerda |
| R | Rotate Right | Rotaciona 90° à direita |
| M | Move | Move 1 posição na direção atual |

**Matriz de Rotações:**

| Direção Atual | Comando L | Comando R |
|---------------|-----------|-----------|
| NORTH | WEST | EAST |
| EAST | NORTH | SOUTH |
| SOUTH | EAST | WEST |
| WEST | SOUTH | NORTH |

**Response:** `200 OK`
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "x": 1,
    "y": 3,
    "direction": "NORTH"
}
```

### Endpoint: Listar Sondas

Retorna o estado atual de todas as sondas registradas no sistema.

**Request:**
```http
GET /probes
```

**Response:** `200 OK`
```json
{
    "probes": {
        "550e8400-e29b-41d4-a716-446655440000": {
            "x": 1,
            "y": 3,
            "direction": "NORTH"
        },
        "6ba7b810-9dad-11d1-80b4-00c04fd430c8": {
            "x": 5,
            "y": 1,
            "direction": "EAST"
        }
    }
}
```

### Códigos de Status HTTP

| Código | Significado | Cenário |
|--------|-------------|---------|
| 200 | OK | Operação executada com sucesso |
| 400 | Bad Request | Movimento inválido ou fora dos limites |
| 404 | Not Found | Sonda não encontrada |
| 422 | Unprocessable Entity | Dados de entrada inválidos |
| 500 | Internal Server Error | Erro interno do servidor |

## Testes

### Executar Suite de Testes

```bash
# Todos os testes
poetry run pytest

# Com output verboso
poetry run pytest -v

# Com relatório de cobertura
poetry run pytest --cov=src --cov-report=html

# Testes específicos por arquivo
poetry run pytest tests/test_probe_service.py

# Testes específicos por função
poetry run pytest tests/test_probe_service.py::test_move_probe_success

# Com marcadores
poetry run pytest -m "not slow"
```

### Estrutura de Testes

| Arquivo | Responsabilidade |
|---------|------------------|
| `test_probe_service.py` | Lógica de negócio e validações |
| `test_probe_repository.py` | Operações de persistência |
| `test_probe_validators.py` | Validação de entrada |

### Persistência de Dados

O sistema utiliza armazenamento em JSON:

```
db/
└── probes.json  # Criado automaticamente na primeira execução
```

**Formato do arquivo:**
```json
{
  "environment": {
    "x": 5,
    "y": 5
  },
  "probes": {
    "probe-id-1": {
      "x": 1,
      "y": 3,
      "direction": "NORTH"
    }
  }
}
```
