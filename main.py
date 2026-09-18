"""API REST de tarefas - CRUD com FastAPI e SQLite."""
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import conectar, criar_tabela


class TarefaEntrada(BaseModel):
    titulo: str
    feita: bool = False


class Tarefa(TarefaEntrada):
    id: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabela()
    yield


app = FastAPI(title="API de Tarefas", lifespan=lifespan)


@app.post("/tarefas", response_model=Tarefa, status_code=201)
def criar_tarefa(tarefa: TarefaEntrada) -> Tarefa:
    with conectar() as conexao:
        cursor = conexao.execute(
            "INSERT INTO tarefas (titulo, feita) VALUES (?, ?)",
            (tarefa.titulo, int(tarefa.feita)),
        )
        return Tarefa(id=cursor.lastrowid, **tarefa.model_dump())


@app.get("/tarefas", response_model=list[Tarefa])
def listar_tarefas(feita: Optional[bool] = None) -> list[Tarefa]:
    with conectar() as conexao:
        if feita is None:
            linhas = conexao.execute("SELECT * FROM tarefas").fetchall()
        else:
            linhas = conexao.execute(
                "SELECT * FROM tarefas WHERE feita = ?", (int(feita),)
            ).fetchall()
    return [Tarefa(id=linha["id"], titulo=linha["titulo"], feita=bool(linha["feita"])) for linha in linhas]


@app.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def buscar_tarefa(tarefa_id: int) -> Tarefa:
    with conectar() as conexao:
        linha = conexao.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,)).fetchone()
    if linha is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return Tarefa(id=linha["id"], titulo=linha["titulo"], feita=bool(linha["feita"]))


@app.put("/tarefas/{tarefa_id}", response_model=Tarefa)
def atualizar_tarefa(tarefa_id: int, tarefa: TarefaEntrada) -> Tarefa:
    with conectar() as conexao:
        cursor = conexao.execute(
            "UPDATE tarefas SET titulo = ?, feita = ? WHERE id = ?",
            (tarefa.titulo, int(tarefa.feita), tarefa_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return Tarefa(id=tarefa_id, **tarefa.model_dump())


@app.delete("/tarefas/{tarefa_id}", status_code=204)
def apagar_tarefa(tarefa_id: int) -> None:
    with conectar() as conexao:
        cursor = conexao.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
