from room.models.tables import Country, Location, Order, Unit


# Moving an actual Unit is done via the Parent Class Unit
# Calling move(order), this changes the location in the database
class Army(Unit):
    def __init__(self,order) -> None:
        super().__init__()
        self.order:Order = order
    
    def validate_move(self)-> bool:
        return True
    
    def validate_support(self) -> bool:
        return True


class Fleet(Unit):
    # HOW TO INITIALISE???????????
    # WANT TO LINK TO EXISTING TABLE ROW
    def __init__(self,order) -> None:
        super().__init__()
        self.order:Order = order

    def validate_move(self) -> bool:
        return True

    def validate_support(self) -> bool:
        return True

    def validate_convoy(self) -> bool:
        return True


# how to initalise correctly? Should this all be in Model?
class Validation(Order):
    def __init__(self) -> None:
        super().__init__()

    # remove orders that are theoritcally possible
    def legitamise_orders(self):
        #move
        #support
        #convoy
        pass

    # calculate tallies 
    def calculate_moves(self):
        # move/support
        # each location added to list and tallied
        pass

    # evalulate tallies
    def evaluate_calulations(self):
        # for each calculation evaluate
        # those that fail, order cancels
        pass

    # record Orders in Outcome table and Move Units
    def perform_operations(self):

        pass
