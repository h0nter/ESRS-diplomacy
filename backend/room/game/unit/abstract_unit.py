from abc import ABC, abstractmethod

# design pattern of factor method
class AbstractUnit(ABC):
    def __init__(self) -> None:
        self.ID
        self.belong
        self.position
        self.can_float
        self.availble_movent
    
    # announce the methods and will be implement in child class
    @abstractmethod
    def move(self):
        pass
    
    @abstractmethod
    def support(self):
        pass
