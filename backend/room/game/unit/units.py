from room.models.tables import Country, Location, Order, Unit

# design pattern of factor method
class UnitParent():
    # constructe with a order model
    def __init__(self, order) -> None:
        self.order:Order = order
        self.unit:Unit = self.order.target_unit
        self.location:Location = self.unit.location
        self.can_float = self.unit.can_float
        self.instruction = self.order.instruction
        self.country:Country = self.unit.owner
    

    # announce the methods and will be implement in child class
    def move(self):
        self.unit.location = self.order.target_location
        self.unit.save()
    
    def support(self):
        pass


class Army(UnitParent):
    def __init__(self, order) -> None:
        super().__init__(order)
    
    def move(self):
        
        pass

    def support(self):
        pass


class Fleet(UnitParent):
    def __init__(self, order) -> None:
        super().__init__(order)

    def move(self):
        super().move()

    def support(self):
        pass

    def convoy(self):
        pass
