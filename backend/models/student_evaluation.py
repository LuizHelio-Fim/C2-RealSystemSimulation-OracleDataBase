from dataclasses import dataclass

@dataclass
class StudentEvaluation:
    id_avaliacao: int  # Composite Primary Key part 1
    id_aluno: int      # Composite Primary Key part 2
    nota: float
