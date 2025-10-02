from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Professor:
    id_professor: Optional[int]  # Auto-generated Primary Key
    cpf: str
    nome: str
    data_nasc: date
    telefone: Optional[str]
    email: str
    status: str
