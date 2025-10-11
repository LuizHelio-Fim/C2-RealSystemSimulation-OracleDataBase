from dataclasses import dataclass
from typing import Optional

@dataclass
class GradeStudent:
    matricula: int    # Student matricula (Changed from id_aluno)
    id_oferta: int    # Offer ID
    status: str       # Status from Student table (auto-populated)