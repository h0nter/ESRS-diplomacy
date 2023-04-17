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

class SituationResolver:
    def __init__(self) -> None:
       self.locationResolvers: dict[str,LocationResolver] = {}

    def add_new_location(self,name):
        if not self.locationResolvers.get(name,False):
            self.locationResolvers[name] = LocationResolver()

    def is_location_in_resolver(self,name):
        return self.locationResolvers.get(name,False)


class ResolverList:
    def __init__(self) -> None:
        self.list: list[SituationResolver] = []

    def add_new_situation(self):
        self.list.append(SituationResolver())
    
    def get_situation_id_by_loc_name(self,name):
        i = 0
        for sit in self.list:
            if sit.is_location_in_resolver(name) != False:
                return i
            else:
                i += 1
        return False

    def add_order_locations(self,order):
        from room.models.order import Order, Location
        if type(order) is Order:
            locations = [order.current_location,order.target_location,
                         order.reference_unit_current_location,order.reference_unit_new_location]
            for location in locations:
                if type(location) is Location:
                    loc_in_sit = self.get_situation_id_by_loc_name(location.name)
                    if loc_in_sit != False:
                        #not equal to false
                        #will add locations if they don't already exist
                        self.list[loc_in_sit].add_new_location(location.name)
                    else:
                        #brand new situation
                        self.add_new_situation()
                        #add location to it
                        self.list[self.get_situation_id_by_loc_name(location.name)].add_new_location(location.name)