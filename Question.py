"""Class Question"""
from abc import ABC, abstractmethod
class Question(ABC):
    """
    generate questions
    """
    def __init__(self) -> None:
        self._question = None
        self._answer = None
        self._question_set = dict()

    @property
    def question_set(self):
        return self._question_set
    
    @abstractmethod
    def add_question(self):
        pass
