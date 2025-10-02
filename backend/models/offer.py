from dataclasses import dataclass
from typing import Optional

@dataclass
class Offer:
    id: Optional[int]  # Auto-generated Primary Key
    ano: int
    semestre: int
    id_materia: int
    id_curso: int
    id_professor: int
