from dataclasses import dataclass
from typing import Optional

@dataclass
class GradeStudent:
    id_aluno: int     # Composite Primary Key part 1
    id_oferta: int    # Composite Primary Key part 2
    status: str
    media_final: Optional[float]