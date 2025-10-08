from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Evaluation:
    id: Optional[int]  # Auto-generated Primary Key
    tipo: str
    peso: float
    data: date
    id_oferta: int
