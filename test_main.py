"""Testes da API de tarefas. Rodar com: pytest"""
import pytest
from fastapi.testclient import TestClient

import database
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def banco_de_teste(tmp_path, monkeypatch):
    # troca o banco antes de cada teste pra não sujar o tarefas.db de verdade
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "teste.db")
    database.criar_tabela()
    yield


def test_cria_e_lista_tarefa():
    resposta = client.post("/tarefas", json={"titulo": "Estudar FastAPI"})
    assert resposta.status_code == 201
    tarefa = resposta.json()
    assert tarefa["titulo"] == "Estudar FastAPI"
    assert tarefa["feita"] is False

    resposta = client.get("/tarefas")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 1


def test_busca_tarefa_inexistente_da_404():
    resposta = client.get("/tarefas/999")
    assert resposta.status_code == 404


def test_atualiza_tarefa():
    criada = client.post("/tarefas", json={"titulo": "Lavar louça"}).json()

    resposta = client.put(f"/tarefas/{criada['id']}", json={"titulo": "Lavar louça", "feita": True})

    assert resposta.status_code == 200
    assert resposta.json()["feita"] is True


def test_apaga_tarefa():
    criada = client.post("/tarefas", json={"titulo": "Apagar depois"}).json()

    resposta = client.delete(f"/tarefas/{criada['id']}")

    assert resposta.status_code == 204
    assert client.get(f"/tarefas/{criada['id']}").status_code == 404


def test_filtra_por_feita():
    client.post("/tarefas", json={"titulo": "Feita", "feita": True})
    client.post("/tarefas", json={"titulo": "Pendente", "feita": False})

    resposta = client.get("/tarefas", params={"feita": True})

    assert len(resposta.json()) == 1
    assert resposta.json()[0]["titulo"] == "Feita"
