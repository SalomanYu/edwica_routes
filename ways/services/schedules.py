from dataclasses import dataclass
from typing import NamedTuple
from pydantic import BaseModel

from datetime import date


class Step(BaseModel):
    profession: str
    deadline: str

class Way(BaseModel):
    deadline: str
    skills: list[str]
    steps: list[Step] 


class DistinctWay(NamedTuple):
    similarId: int
    resumeId: str
    skills: list[str]
    deadline: str
    steps: list[Step]


@dataclass(slots=True)
class ProfessionStep:
    title: str
    experiencePost: str
    experienceInterval: str
    experienceDuration: str
    branch: str
    subbranch: str
    weightInGroup: int
    level: int
    levelInGroup: int
    groupId: int
    area: str
    city: str
    generalExcepience: str
    specialization: str
    salary: str
    educationUniversity: str
    educationDirection: str
    educationYear: str # Потому что может быть перечисление
    languages: str
    skills: str
    advancedTrainingTitle: str
    advancedTrainingDirection: str
    advancedTrainingYear: str
    dateUpdate: date
    resumeId: str
    similarPathId: int | None = None
    db_id: set | None = None # Эта переменная отвечает за айди конкретного этапа. Он будет использоваться только внутри програмы, в бд эта константа проставляется автоматически (id)


class ResumeGroup(NamedTuple): # Класс, который хранит информацию о резюме в виде айди резюме и списка разложенных этапов в карьере
    ID: str # Ссылка резюме
    ITEMS: tuple[ProfessionStep]