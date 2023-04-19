from django.db import models

# manages grabbing data from db
class OutcomeManager(models.Manager):
    # Move Units after resolve
    def perform_move_operations(self,turn):
        from room.models.order import OutcomeType, MoveType, Turn
        if type(turn) is Turn:
            for successful_outcome in self.get_queryset().filter(validation=OutcomeType.PASS)\
                    .filter(order_reference__turn=turn).filter(order_reference__instruction=MoveType.MOVE):
                successful_outcome.order_reference.target_unit.move(successful_outcome.order_reference.target_location)
        else:
            raise TypeError('Type should be Turn')
        
    def _grab_this_turn_maybe_orders(self,turn):
        from room.models.order import OutcomeType
        # only selecting orders yet to be evaluated
        return self.get_queryset().filter(order_reference__turn=turn).filter(validation=OutcomeType.MAYBE)

    def _grab_spt_attacking_orders(self,location,turn):
        from room.models.order import MoveType
        # we grab the support moves that reference this new location
        # this means the referenced unit is Moving to this location
        return self._grab_this_turn_maybe_orders(turn)\
            .filter(order_reference__instruction=MoveType.SUPPORT)\
            .filter(order_reference__reference_unit_new_location=location)
    
    def _grab_mve_attacking_orders(self,location,turn):
        from room.models.order import MoveType
        # we grab the moves that reference this location
        return self._grab_this_turn_maybe_orders(turn)\
            .filter(order_reference__instruction=MoveType.MOVE)\
            .filter(order_reference__target_location=location)

    # grabs all attacking orders that reference the location specified
    def grab_all_attacking_orders(self,location,turn):
        from room.models.locations import Location
        from room.models.order import Turn
        if type(location) is Location and type(turn) is Turn:
            return self._grab_mve_attacking_orders(location,turn).union(
                self._grab_spt_attacking_orders(location,turn))
        else:
            raise TypeError('location Type should be Location and turn Type should be Turn')
        
    def grab_order_current_location(self,location,turn):
        # we grab the orders that reference this location as current
        from room.models.locations import Location
        from room.models.order import Turn
        if type(location) is Location and type(turn) is Turn:
            return self._grab_this_turn_maybe_orders(turn)\
                .filter(order_reference__current_location=location)
        else:
            raise TypeError('location Type should be Location and turn Type should be Turn')
        
    def _grab_spt_defence_orders(self,location,turn):
        from room.models.order import MoveType
        # we grab the support moves that reference this as current location
        # this means the referenced unit is staying at this location
        return self._grab_this_turn_maybe_orders(turn)\
            .filter(order_reference__instruction=MoveType.SUPPORT)\
            .filter(order_reference__reference_unit_current_location=location)\
            .filter(order_reference__reference_unit_new_location=None)
    
    def grab_all_defence_orders(self,location,turn):
        from room.models.locations import Location
        from room.models.order import Turn
        if type(location) is Location and type(turn) is Turn:
            return self._grab_spt_defence_orders(location,turn).union(
                self.grab_order_current_location(location,turn))
        else:
            raise TypeError('location Type should be Location and turn Type should be Turn')
        
    def grab_all_mve_orders(self,turn):
        from room.models.order import Turn, MoveType
        if type(turn) is Turn:
            return self._grab_this_turn_maybe_orders(turn) \
                .filter(order_reference__instruction=MoveType.MOVE)
        else:
            raise TypeError('Type should be Turn')
