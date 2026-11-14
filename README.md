# Vendas API

API responsável pelo gerenciamento do processo de vendas de uma plataforma de revenda de veículos, desenvolvida em Python com FastAPI e PostgreSQL.

## Tecnologias

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL 16
- Alembic
- Docker e Docker Compose
- Pytest
- Ruff

## Funcionalidades

- Solicitação de compra de veículos.
- Registro e acompanhamento de vendas.
- Processamento de notificações de pagamento.
- Atualização do status da venda conforme o resultado do pagamento.
- Listagem de veículos disponíveis e vendidos.
- Integração HTTP com o microsserviço de veículos.

## Estrutura do projeto

O serviço utiliza uma arquitetura baseada em Domain-Driven Design (DDD), organizada em:

- `domain`: entidades e regras de negócio.
- `application`: casos de uso e interfaces.
- `infrastructure`: banco de dados, repositórios e integrações.
- `interfaces`: rotas e schemas da API.
- `alembic`: versionamento do banco de dados com Alembic.
- `tests`: testes automatizados.

## Como executar

### Pré-requisitos

- Docker
- Docker Compose

### Inicialização

O serviço depende da rede Docker compartilhada `microsservicos`, criada pelo `veiculos-api`. Portanto, inicie primeiro o serviço de veículos:

Inicie o serviço de vendas:

```bash
docker compose up -d --build
```

O Docker Compose inicia a API e seu PostgreSQL independente. As migrations do Alembic são executadas automaticamente antes da inicialização da aplicação.

A API estará disponível em:

- API: http://localhost:8001
- Swagger: http://localhost:8001/docs
- Health check: http://localhost:8001/health

Para visualizar os logs:

```bash
docker compose logs -f api
```

Para interromper os serviços:

```bash
docker compose down
```

## Endpoints

### Compras

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/compras` | Solicita uma compra de veículo |
| GET | `/compras` | Lista as vendas registradas |

### Veículos

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/veiculos/disponiveis` | Lista os veículos disponíveis |
| GET | `/veiculos/vendidos` | Lista os veículos vendidos |

### Health check

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/health` | Verifica a saúde da aplicação |

Para consultar os parâmetros, schemas e respostas de cada endpoint, acesse o Swagger.

## Banco de dados

O serviço utiliza um banco PostgreSQL independente do `veiculos-api`, garantindo a segregação dos dados entre os microsserviços.

As alterações no esquema do banco são controladas pelo Alembic. As migrations pendentes são executadas automaticamente durante a inicialização do container.

## Testes e qualidade

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute os testes:

```bash
pytest
```

Execute a análise de cobertura:

```bash
pytest --cov=app --cov-branch --cov-report=term-missing
```

Execute o Ruff:

```bash
ruff check app tests
```

## CI/CD

O projeto utiliza GitHub Actions para automação de integração e entrega contínua.

- **CI:** executa análise estática com Ruff e testes automatizados em Pull Requests e atualizações da branch `main`.
- **CD:** após a conclusão bem-sucedida do CI na `main`, constrói a imagem Docker, cria a rede compartilhada, inicia os containers, verifica o endpoint `/health` e realiza a limpeza do ambiente de execução.

## Integração com outros serviços

Este microsserviço integra-se ao `veiculos-api` por meio de comunicação HTTP.

O serviço de veículos é responsável pelo cadastro e gerenciamento dos veículos. O serviço de vendas consulta essas informações e registra as compras em seu próprio banco de dados.

A comunicação entre os containers utiliza a rede Docker compartilhada `microsservicos`.