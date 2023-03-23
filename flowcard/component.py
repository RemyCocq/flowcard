from abc import ABC, abstractmethod


class Component(ABC):
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