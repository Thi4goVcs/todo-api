"""Acesso ao banco SQLite usado pela API de tarefas."""
import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).parent / "tarefas.db"


def conectar(db_path: Optional[Path] = None) -> sqlite3.Connection:
    # lê DB_PATH aqui dentro (e não como valor padrão do parâmetro) pra dar
    # pra trocar o banco em teste com monkeypatch sem precisar passar argumento
    conexao = sqlite3.connect(db_path or DB_PATH)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela(db_path: Optional[Path] = None) -> None:
    with conectar(db_path) as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                feita INTEGER NOT NULL DEFAULT 0
            )
            """
        )
