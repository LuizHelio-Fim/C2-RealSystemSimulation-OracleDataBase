from dataclasses import dataclass
from typing import Optional

@dataclass
class GradeStudent:
    matricula: int    # Student matricula (ID_ALUNO references ALUNO.MATRICULA)
    id_oferta: int    # Offer ID 
    status: str       # Status from Student table (Ativo, Trancado, Formado)
    # media_final removida - sistema de notas eliminado