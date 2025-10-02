from dataclasses import dataclass
from typing import Optional

@dataclass
class Subject:
    id_materia: int  # Composite Primary Key part 1
    id_curso: int    # Composite Primary Key part 2
    periodo: int
    nome: str
    carga_horaria: int
    media_aprovacao: float
