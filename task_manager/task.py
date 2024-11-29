# -*- coding: utf-8 -*-
from typing import List, Dict
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    id: int
    title: str
    description: str
    category: str
    due_date: str
    priority: str
    status: str = "Не выполнена"

    def to_dict(self) -> Dict:
        return self.__dict__

    @staticmethod
    def from_dict(data: Dict) -> 'Task':
        return Task(**data)
