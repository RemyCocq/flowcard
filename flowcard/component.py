from abc import ABC, abstractmethod


class Component(ABC):
    @classmethod
    @property
    @abstractmethod
    def name(cls) -> str:
        raise NotImplemented

    def __init__(self):
        pass

    @abstractmethod
    def to_html(self):
        pass

    @abstractmethod
    def to_markdown(self):
        pass


class Container(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def to_html(self):
        pass

    @abstractmethod
    def to_markdown(self):
        pass
