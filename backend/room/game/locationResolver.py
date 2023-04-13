# allows to resolve orders
class LocationResolver:
    def __init__(self) -> None:
        from room.models.order import Order
        # list of orders defending
        self.defending: list[Order] = []
        # dict of country and orders attacking
        self.attacking: dict[str, list[Order]] = {}
        # the current unit in location this turn
        self.current_unit_order: Order|None = None
        self.current_unit_moved: bool = False

    # returns length of defence list
    def get_defence_amount(self) -> int:
        return len(self.defending)

    # adds order to defence if not already in the list
    def add_to_defence(self,order) -> None:
        if order not in self.defending:
            self.defending.append(order)    
    
    # grabs the attacking amount using unit
    def get_attacking_amount(self,unit) -> int:
        from room.game.unitTypes import Unit
        if type(unit) is Unit:
            country = unit.owner.name
            return len(self.attacking[country])
        raise TypeError('Type should be Unit')

    
    # adds order to attacking if not already in the dict
    def add_to_attacking(self,unit,order) -> None:
        from room.game.unitTypes import Unit
        if type(unit) is Unit:
            country = unit.owner.name
            if country in self.attacking:
                if order not in self.attacking[country]:
                    self.attacking[country].append(order)
            else:
                self.attacking[country] = [order]

    
