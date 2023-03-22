from abc import ABC, abstractmethod
from room.models.tables import Country, Location, Order, Unit


# design pattern of factor method
class AbstractUnit(ABC):
    # constructe with a order model
    def __init__(self, order) -> None:
        self.order:Order = order
        self.unit:Unit = self.order.target_unit
        self.location:Location = self.unit.location
        self.can_float = self.unit.can_float
        self.instruction = self.order.instruction
        self.country:Country = self.unit.owner
    

    # announce the methods and will be implement in child class
    @abstractmethod
    def move(self):
        #self.location:Location = self.order.target_location
        self.unit.save()
    
    @abstractmethod
    def support(self):
        pass
