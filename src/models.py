from typing import List
from pydantic import BaseModel


class Experiment(BaseModel):
    name: str
    content: str


class Experiments(BaseModel):
    configurations: List[Experiment]