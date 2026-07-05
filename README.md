# Backend Parking Lot

API para gerenciamento de um estacionamento: cadastro da configuração do local
(área, capacidade e preço por hora) e controle das vagas numeradas (ocupação
e liberação).

---
## Como executar

Após clonar o repositório, acesse o diretório raiz do projeto pelo terminal
para executar os comandos abaixo.

### 1. Criar e ativar um ambiente virtual

> É fortemente indicado o uso de ambientes virtuais, como o
> [venv](https://docs.python.org/3/library/venv.html).

No Windows (PowerShell):
```
python -m venv .venv
.venv\Scripts\Activate.ps1
```

No Linux/macOS:
```
python -m venv .venv
source .venv/bin/activate
```

### 2. Instalar as dependências

```
(.venv)$ pip install -r requirements.txt
```

### 3. Executar a aplicação

```
(.venv)$ python app.py
```

Ou, alternativamente, usando o CLI do Flask (com reload automático a cada
mudança no código):

```
(.venv)$ flask run --host 0.0.0.0 --port 5000 --reload
```

O banco de dados SQLite (`database/db.sqlite3`) e suas tabelas são criados
automaticamente na primeira execução.

### 4. Acessar a aplicação

Com o servidor rodando, abra [http://localhost:5000/](http://localhost:5000/)
no navegador. A documentação interativa (Swagger) fica disponível em
[http://localhost:5000/openapi/swagger](http://localhost:5000/openapi/swagger).

---
## Rotas disponíveis

### Configuração do estacionamento

| Método | Rota            | Descrição                                        |
|--------|-----------------|--------------------------------------------------|
| GET    | `/configuracao` | Retorna a configuração cadastrada                |
| POST   | `/configuracao` | Cadastra a configuração (única) e gera as vagas  |
| PUT    | `/configuracao` | Atualiza a configuração e ajusta as vagas        |

Corpo esperado (POST/PUT):
```json
{
  "area": 500.0,
  "capacidade": 50,
  "preco_hora": 5.0
}
```

### Vagas

| Método | Rota                     | Descrição                           |
|--------|--------------------------|-------------------------------------|
| GET    | `/vagas`                 | Lista todas as vagas                |
| GET    | `/vagas/<numero>`        | Detalha uma vaga específica         |
| PUT    | `/vagas/<numero>/ocupar` | Ocupa a vaga com a placa informada  |
| PUT    | `/vagas/<numero>/liberar`| Libera a vaga                       |

Corpo esperado (PUT `/vagas/<numero>/ocupar`):
```json
{
  "placa": "ABC1D23"
}
```
