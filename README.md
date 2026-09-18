# todo-api

API de tarefas em Python. CRUD simples: cria, lista, busca uma, atualiza e apaga. Banco é SQLite, sem servidor externo pra configurar.

Segundo projeto do portfólio, um dia depois do organizador de arquivos. Sempre achei API o tipo de coisa "avançada demais pra mim" e resolvi só testar — deu pra fazer funcionando em uma sessão.

## Rodando

```bash
git clone https://github.com/Thi4goVcs/todo-api.git
cd todo-api
pip install -r requirements.txt
uvicorn main:app --reload
```

Com o servidor no ar, a documentação interativa fica em `http://127.0.0.1:8000/docs` — dá pra testar os endpoints direto no navegador, sem precisar de Postman.

## Endpoints

```
POST   /tarefas            cria tarefa
GET    /tarefas             lista todas (aceita ?feita=true ou ?feita=false)
GET    /tarefas/{id}        busca uma
PUT    /tarefas/{id}        atualiza
DELETE /tarefas/{id}        apaga
```

## Testes

```bash
pytest
```

Os testes usam um banco temporário (`tmp_path` do pytest), então não mexem no `tarefas.db` de verdade.

## Algumas coisas que decidi no caminho

Separei o acesso ao banco (`database.py`) da parte da API (`main.py`) — achei mais fácil de entender assim do que tudo misturado num arquivo só.

A tabela do banco é criada automaticamente quando o servidor sobe (função de startup do FastAPI), então não precisa rodar nenhum script de setup antes.
