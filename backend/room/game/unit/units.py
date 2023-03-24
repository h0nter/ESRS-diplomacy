from room.game.unit.abstract_unit import AbstractUnit
from room.models.tables import Country, Location, Order, Unit

class Army(Unit):
    def __init__(self, order) -> None:
        super().__init__(order)
    
    def move(self):
        super().move()
        pass

    def support(self):
        super().support()
        pass


class Fleet(AbstractUnit):
    def __init__(self, order) -> None:
        super().__init__(order)

    def move(self):
        super().move()

    def support(self):
        pass

    def convoy(self):
        pass
