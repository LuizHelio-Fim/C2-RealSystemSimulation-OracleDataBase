from dataclasses import dataclass
from typing import Optional

@dataclass
class Course:
    id: Optional[int]  # Auto-generated Primary Key
    nome: str
    carga_horaria_total: int
