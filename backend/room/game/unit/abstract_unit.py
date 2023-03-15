from abc import ABC, abstractmethod

# design pattern of factor method
class AbstractUnit(ABC):
    def __init__(self) -> None:
        self.ID
        self.current_location
        self.target_location
        self.instruction
    
    # announce the methods and will be implement in child class
    @abstractmethod
    def move(self):
        pass
    
    @abstractmethod
    def support(self):
        pass
