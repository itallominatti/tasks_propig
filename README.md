# Tasks Propig

Tasks Propig é uma API RESTful desenvolvida em Python utilizando Django e Django REST Framework, focada no gerenciamento seguro de usuários e tarefas (tasks). O projeto adota autenticação JWT, arquitetura em camadas e princípios de Domain-Driven Design (DDD), visando escalabilidade, organização e facilidade de manutenção.

---

## Sumário

- [Visão Geral](#visão-geral)
- [System Design e Arquitetura](#system-design-e-arquitetura)
- [Como baixar e rodar o projeto](#como-baixar-e-rodar-o-projeto)
- [Acessando o ElasticSearch](#acessando-o-elasticsearch)
- [Principais Endpoints](#principais-endpoints)
- [Exemplos de uso com cURL](#exemplos-de-uso-com-curl)
- [Rodando os testes](#rodando-os-testes)
- [Estrutura de Pastas](#estrutura-de-pastas)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

---

## Visão Geral

Tasks Propig oferece endpoints para cadastro, autenticação e gerenciamento de usuários e tarefas. Cada usuário pode criar, visualizar, atualizar e deletar apenas suas próprias tasks, garantindo privacidade e segurança. O projeto é ideal para quem busca um exemplo prático de API moderna, segura e bem estruturada.

**Principais recursos:**
- Cadastro e autenticação de usuários com JWT.
- Gerenciamento completo de tarefas (CRUD).
- Isolamento de domínios (usuário e task).
- Testes automatizados com Pytest e APITestCase.
- Documentação automática com Swagger.
- HATEOAS para facilitar navegação entre recursos.
- Arquitetura em camadas baseada em DDD.

---

## System Design e Arquitetura

- **Arquitetura em Camadas & DDD:**  
  O projeto é dividido em camadas, separando regras de negócio, infraestrutura e apresentação. Utiliza Domain-Driven Design para organizar entidades, casos de uso e repositórios.
  - `core/`: Entidades de domínio, interfaces de repositório e casos de uso.
  - `adapters/`: Implementações para hash de senha, JWT e integrações externas.
  - `django_project/`: Apps Django para REST API, autenticação, usuários e tasks.

- **Autenticação JWT:**  
  Usuários autenticam via `/auth/login/` e recebem um token JWT, necessário para acessar endpoints protegidos.

- **Isolamento de Domínios:**  
  Usuário e Task são domínios independentes. Tasks referenciam o usuário dono, mas não há acoplamento direto reverso.

- **Testes Automatizados:**  
  Utiliza `pytest` e `APITestCase` para garantir a qualidade dos endpoints e regras de negócio.

- **Documentação Automática:**  
  Swagger disponível em `/swagger/` para explorar e testar a API.

- **HATEOAS:**  
  Os endpoints seguem o princípio HATEOAS (Hypermedia as the Engine of Application State), fornecendo links de navegação nas respostas para facilitar a descoberta e interação com os recursos da API.

---

## Como baixar e rodar o projeto

### Pré-requisitos

- Docker e Docker Compose

### Passos para rodar com Docker

1. **Configure as variáveis de ambiente:**
  - Copie o arquivo de exemplo:
    ```sh
    cp .env-example .env
    ```
  - Edite `.env` conforme necessário (credenciais do banco, secret key, etc).

2. **Suba a aplicação e o banco de dados com Docker Compose:**
  ```sh
  docker compose up --build
  ```

3. **Acesse a aplicação:**
  - O backend estará disponível em [http://localhost:8000/](http://localhost:8000/)
  - A documentação Swagger estará em [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

4. **(Opcional) Executar comandos no container:**
  - Para rodar migrações manualmente:
    ```sh
    docker compose exec web poetry run python manage.py migrate
    ```
  - Para criar um superusuário:
    ```sh
    docker compose exec web poetry run python manage.py createsuperuser
    ```

---

## Acessando o ElasticSearch

O projeto inclui um serviço ElasticSearch para indexação e busca de dados.

- **Host:** [http://localhost:9200/](http://localhost:9200/)
- **Usuário padrão:** `elastic`
- **Senha padrão:** `changeme` (ou conforme definido no seu `.env` ou `docker-compose.yml`)

### Como acessar o ElasticSearch

1. **Via navegador:**  
   Acesse [http://localhost:9200/](http://localhost:9200/) para verificar se o serviço está rodando.

2. **Via cURL:**  
   ```sh
   curl -u elastic:changeme http://localhost:9200/
   ```

3. **Via Kibana (se disponível):**  
   Caso o serviço Kibana esteja configurado no seu `docker-compose.yml`, acesse [http://localhost:5601/](http://localhost:5601/) para uma interface web de gerenciamento.

> **Importante:**  
> Altere a senha padrão do ElasticSearch em ambientes de produção.

---

## Principais Endpoints

- `POST /api/users/` — Cadastro de usuário
- `POST /auth/login/` — Autenticação e obtenção do JWT
- `GET /api/tasks/` — Listar tasks do usuário
- `POST /api/tasks/` — Criar nova task
- `PUT /api/tasks/{id}/` — Atualizar task
- `DELETE /api/tasks/{id}/` — Remover task

Consulte a documentação Swagger em `/swagger/` para detalhes completos.

---

## Exemplos de uso com cURL

### Cadastro de usuário

```sh
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "password": "securepassword123", "email": "usuario@gmail.com"}'
```

### Autenticação (obter JWT)

```sh
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "password": "securepassword123"}'
```

A resposta conterá um campo `token` com o token JWT. Guarde esse token para autenticar as próximas requisições.

### Listar tasks do usuário

```sh
curl -X GET http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer SEU_TOKEN_JWT"
```

### Criar nova task

```sh
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer SEU_TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{"title": "Minha nova task", "description": "Descrição opcional"}'
```

### Atualizar uma task

```sh
curl -X PUT http://localhost:8000/api/tasks/1/ \
  -H "Authorization: Bearer SEU_TOKEN_JWT" \
  -H "Content-Type: application/json" \
  -d '{"title": "Título atualizado", "description": "Nova descrição"}'
```

### Remover uma task

```sh
curl -X DELETE http://localhost:8000/api/tasks/1/ \
  -H "Authorization: Bearer SEU_TOKEN_JWT"
```

---

## Rodando os testes

Execute todos os testes automatizados com Docker:

```sh
docker compose exec web /app/.venv/bin/python -m pytest
```

---

## Estrutura de Pastas

```
tasks_propig/
├── core/           # Domínio, entidades, casos de uso
├── adapters/       # Integrações (hash, JWT, etc)
├── django_project/
│   ├── users/      # App de usuários
│   ├── tasks/      # App de tasks
│   └── ...         # Configurações Django
├── tests/          # Testes automatizados
├── .env-example    # Exemplo de variáveis de ambiente
├── Dockerfile
├── docker-compose.yml
└── README.md
```

