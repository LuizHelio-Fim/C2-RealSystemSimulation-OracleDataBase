from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Student:
    id: int
    matricula: str
    cpf: Optional[str]
    nome: str
    data_nascimento: date
    telefone: Optional[str]
    email: str
    periodo: int
    id_curso: int
    status_curso: Optional[str] = None