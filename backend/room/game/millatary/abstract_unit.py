from abc import ABC, abstractmethod

class Abstract_unit(ABC):
    def __init__(self) -> None:
        self.ID
        self.belong
        self.position
        self.availble_movent
        
    @abstractmethod
    def move(self):
        pass
    
    @abstractmethod
    def support(self):
        pass

    @abstractmethod
    def attend(self):
        pass