from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Student:
    matricula: int  # Primary Key
    cpf: str
    nome: str
    data_nasc: date
    telefone: str
    email: str
    periodo: int
    id_curso: int
    status_curso: str