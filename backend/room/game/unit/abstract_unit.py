from abc import ABC, abstractmethod


# design pattern of factor method
class AbstractUnit(ABC):
    # constructe with a order model
    def __init__(self, order) -> None:
        self.order = order
        self.unit = order.target_unit
        self.location = self.unit.location
        self.can_float = self.unit.can_float
        self.instruction = self.order.instruction
        self.country = self.unit.owner
    
    # announce the methods and will be implement in child class
    @abstractmethod
    def move(self):
        self.location = self.order.target_location
        self.unit.save()
    
    @abstractmethod
    def support(self):
        pass
