from django.db import models

# manages grabbing data from db
class OutcomeManager(models.Manager):
    # Move Units after resolve
    def perform_move_operations(self,turn,room):
        from room.models.order import MoveType
        from room.models.turn import Turn
        from room.models.outcome import OutcomeType
        from room.models.room import Room
        if isinstance(turn,Turn) and isinstance(room,Room):
            for successful_outcome in self.get_queryset().filter(validation=OutcomeType.PASS)\
                    .filter(order_reference__turn=turn).filter(order_reference__room=room) \
                    .filter(order_reference__instruction=MoveType.MOVE):
                successful_outcome.order_reference.unit.move(successful_outcome.order_reference.target_location)
        else:
            raise TypeError('Type should be Turn')
        
    def _grab_this_turn_maybe_orders(self,turn,room):
        from room.models.outcome import OutcomeType
        # only selecting orders yet to be evaluated
        return self.get_queryset().filter(order_reference__turn=turn).filter(order_reference__room=room).filter(validation=OutcomeType.MAYBE)

    def grab_spt_attacking_orders(self,location,turn,room):
        from room.models.order import MoveType
        from room.models.turn import Turn
        from room.models.location import Location
        from room.models.room import Room
        # we grab the support moves that reference this new location
        # this means the referenced unit is Moving to this location
        if isinstance(turn,Turn) and isinstance(location,Location) and isinstance(room,Room):
            return self._grab_this_turn_maybe_orders(turn,room)\
                .filter(order_reference__instruction=MoveType.SUPPORT)\
                .filter(order_reference__reference_unit_new_location=location)
        else:
            raise TypeError('turn Type should be Turn and location Type ({}) should be Location'.format(type(location)))
    
    def _grab_related_spt_orders(self,order,turn,room):
        from room.models.order import MoveType
        from room.models.outcome import OutcomeType
        return (models.Q(order_reference__room=room) & models.Q(order_reference__turn=turn) & models.Q(validation=OutcomeType.MAYBE)
                    & models.Q(order_reference__instruction=MoveType.SUPPORT)
                    & models.Q(order_reference__reference_unit=order.unit)
                    & models.Q(order_reference__reference_unit_current_location=order.current_location)
                    & models.Q(order_reference__reference_unit_new_location=order.target_location)
                )
        
    def grab_related_spt_orders(self,order,turn,room):
        from room.models.turn import Turn
        from room.models.order import Order
        from room.models.room import Room
        if isinstance(turn,Turn) and isinstance(room,Room) and isinstance(order,Order):
            return self.get_queryset().filter(self._grab_related_spt_orders(order,turn,room))
        else:
            raise TypeError('turn Type: {} should be Turn and order Type: {} should be Order'.format(type(turn),type(order)))

    
    def _grab_mve_attacking_orders(self,location,turn,room,include_bounce=False):
        from room.models.order import MoveType
        from room.models.outcome import OutcomeType
        from room.models.location import Location
        # we grab the moves that reference this location
        if isinstance(location,Location):
            if include_bounce:
                query = (models.Q(order_reference__room=room) & models.Q(order_reference__turn=turn) & 
                         (models.Q(validation=OutcomeType.BOUNCE) | models.Q(validation=OutcomeType.MAYBE)))
            else:
                query = (models.Q(order_reference__room=room) & models.Q(order_reference__turn=turn) & models.Q(validation=OutcomeType.MAYBE))

            return (query & models.Q(order_reference__instruction=MoveType.MOVE) & 
                     models.Q(order_reference__target_location=location))
        else:
            raise TypeError('location Type should be Location')
        
    def grab_mve_attacking_orders(self,location,turn,room,include_bounce=False):
        from room.models.turn import Turn
        from room.models.location import Location
        from room.models.room import Room
        if isinstance(turn,Turn) and isinstance(location,Location) and isinstance(room,Room):
            return self.get_queryset().filter(
                self._grab_mve_attacking_orders(location,turn,room,include_bounce=include_bounce))
        else:
            raise TypeError('turn Type should be Turn and location Type should be Location')
        
    # grabs all attacking orders that reference the location specified
    def grab_attacking_strength_of_order(self,order,turn,room,include_bounce=False):
        from room.models.turn import Turn
        from room.models.order import Order
        from room.models.outcome import OutcomeType
        from room.models.room import Room
        if isinstance(turn,Turn) and isinstance(order,Order) and isinstance(room,Room):
            if not include_bounce:
                outcome_query = (models.Q(order_reference__room=room) &
                                 models.Q(order_reference__turn=turn) & 
                                 models.Q(validation=OutcomeType.MAYBE) &
                                 models.Q(order_reference__unit = order.unit))
            else:
                outcome_query = (models.Q(order_reference__room=room) &
                                 models.Q(order_reference__turn=turn) & 
                                 models.Q(validation=OutcomeType.BOUNCE) &
                                 models.Q(order_reference__unit = order.unit))
            return self.get_queryset().filter(outcome_query | self._grab_related_spt_orders(order,turn,room))
        else:
            raise TypeError('turn Type should be Turn and order Type ({}) should be Order'.format(type(order)))
        
    def grab_highest_attacking_mve(self,location,turn,room,include_bounce=False):
        from room.models.location import Location
        from room.models.turn import Turn
        from room.models.room import Room
        if isinstance(turn,Turn) and isinstance(location,Location) and isinstance(room,Room):
            attacks = self._grab_mve_attacking_orders(location,turn,room,include_bounce=include_bounce)
            max_attack_strength = 0
            max_attack = []
            for attack in self.get_queryset().filter(attacks):
                strength = self.grab_attacking_strength_of_order(attack.order_reference,turn,room,include_bounce=include_bounce)
                if len(strength) == max_attack_strength:
                    max_attack.append(attack)
                elif len(strength) > max_attack_strength:
                    max_attack = [attack]
                    max_attack_strength = len(strength)
            return max_attack
        else:
            raise TypeError('location Type should be Location and turn Type should be Turn')
        
    def _grab_outcome_current_location(self,location,turn,room):
        # we grab the orders that reference this location as current
        from room.models.location import Location
        from room.models.turn import Turn
        from room.models.room import Room
        if isinstance(turn,Turn) and isinstance(location,Location) and isinstance(room,Room):
            # doesn't matter if it is void or not
            return (models.Q(order_reference__room=room) & models.Q(order_reference__turn=turn) & 
                     models.Q(order_reference__current_location=location))
        else:
            raise TypeError('location Type should be Location and turn Type should be Turn')
        
    def grab_outcome_current_location(self,location,turn,room):
        from room.models.location import Location
        from room.models.turn import Turn
        from room.models.room import Room
        if isinstance(turn,Turn) and isinstance(location,Location) and isinstance(room,Room):
            return self.get_queryset().filter(self._grab_outcome_current_location(location,turn,room))
        else:
            raise TypeError('location Type should be Location and turn Type should be Turn')
        
    def _grab_defender_current_location(self,location,turn,room):
        from room.models.order import MoveType
        from room.models.outcome import OutcomeType
        # if the order is moving away from spot, it is no longer defending
        return (models.Q(order_reference__room=room) & models.Q(order_reference__turn=turn) & 
                     models.Q(order_reference__current_location=location) & 
                     ~(models.Q(order_reference__instruction=MoveType.MOVE) & 
                      models.Q(validation=OutcomeType.MAYBE)))
        
    def grab_defender_current_location(self,location,turn,room):
        from room.models.location import Location
        from room.models.turn import Turn
        from room.models.room import Room
        if isinstance(turn,Turn) and isinstance(location,Location) and isinstance(room,Room):
            return self.get_queryset().filter(self._grab_defender_current_location(location,turn,room))
        else:
            raise TypeError('location Type should be Location and turn Type should be Turn')
        
    def _grab_spt_defence_orders(self,location,turn,room):
        from room.models.order import MoveType
        from room.models.outcome import OutcomeType
        # we grab the support moves that reference this as current location
        # this means the referenced unit is staying at this location
        return (models.Q(order_reference__room=room) & models.Q(order_reference__turn=turn) & 
                models.Q(validation=OutcomeType.MAYBE) &
                models.Q(order_reference__instruction=MoveType.SUPPORT) &
                models.Q(order_reference__reference_unit_current_location=location) &
                models.Q(order_reference__reference_unit_new_location=None))
    
    def grab_all_defence_orders(self,location,turn,room):
        from room.models.location import Location
        from room.models.turn import Turn
        from room.models.room import Room
        if isinstance(turn,Turn) and isinstance(location,Location) and isinstance(room,Room):
            return self.get_queryset().filter(self._grab_spt_defence_orders(location,turn,room) |
                    self._grab_defender_current_location(location,turn,room))
        else:
            raise TypeError('location Type should be Location and turn Type should be Turn')
        
    def grab_all_mve_orders(self,turn,room):
        from room.models.turn import Turn
        from room.models.order import MoveType
        from room.models.room import Room
        if isinstance(turn,Turn) and isinstance(room,Room):
            return self._grab_this_turn_maybe_orders(turn,room) \
                .filter(order_reference__instruction=MoveType.MOVE)
        else:
            raise TypeError('Type should be Turn')
        

    def grab_convoy_orders_for_order(self,turn,room,order):
        from room.models.order import MoveType
        from room.models.turn import Turn
        from room.models.order import Order
        from room.models.room import Room
        if isinstance(turn,Turn) and isinstance(room,Room) and isinstance(order,Order):
            return self._grab_this_turn_maybe_orders(turn,room) \
                .filter(order_reference__instruction=MoveType.CONVOY) \
                .filter(order_reference__reference_unit=order.unit)
        else:
            raise TypeError('turn Type should be Turn and order Type should be Order')
    
    # private as only needed for working out if alternative route
    def _convoy_dfs(self, node, target, graph, visited=set()):
        #print(node,target,graph)
        visited.add(node)
        if node == target:
            return True
        elif node in graph:
            for child in graph[node]:
                if child not in visited:  # Check whether the node is visited or not
                    result = self._convoy_dfs(child, target, graph, visited)  
                    # Call the dfs recursively
                    
                    if result is True:
                        return True
                
        return False

    def is_alternative_convoy_route(self,turn,room,order,location):
        from room.models.location import Location, Next_to
        from room.models.turn import Turn
        from room.models.order import Order
        from room.models.room import Room
        if isinstance(turn,Turn) and isinstance(room,Room) and isinstance(location,Location) and isinstance(order,Order):
            related_convoys = self.grab_convoy_orders_for_order(turn,room,order)\
                .exclude(order_reference__current_location=location) #remove node to avoid
            graph = {}
            # add current and last locations
            graph[order.current_location.pk] = \
                    list(Next_to.objects.filter(location=order.current_location).values_list('next_to__pk',flat=True))
            if order.target_location is None: raise TypeError('order not MVE')
            graph[order.target_location.pk] = \
                    list(Next_to.objects.filter(location=order.target_location).values_list('next_to__pk',flat=True))
            # add convoy locations
            for convoy in related_convoys:
                # create a graph of pks, similar to '1':['2','3','4']
                graph[convoy.order_reference.current_location.pk] = \
                    list(Next_to.objects.filter(location=convoy.order_reference.current_location).values_list('next_to__pk',flat=True))
            #print('graph',graph)
            # convoy success regardless of location, means alternative route
            return self._convoy_dfs(order.current_location.pk,order.target_location.pk,graph)
        else:
            raise TypeError('location Type:{} should be Location and turn Type:{} should be Turn and order Type{} should be Order'.format(type(location),type(turn),type(order)))
        
    def grab_all_cvy_mve_orders(self,turn,room,add_marked=False):
        from room.models.turn import Turn
        from room.models.order import Order, MoveType
        from room.models.outcome import OutcomeType
        from room.models.room import Room
        if isinstance(turn,Turn) and isinstance(room,Room):
            moves = (models.Q(order_reference__room=room) & models.Q(order_reference__turn=turn) & 
                     models.Q(order_reference__instruction=MoveType.MOVE))
            if add_marked: 
                moves = (moves & (models.Q(validation=OutcomeType.MAYBE) | 
                                  models.Q(validation=OutcomeType.MARK)))
            else:
                moves = (moves & models.Q(validation=OutcomeType.MAYBE))
                               
            # work out a filter to remove all but cvy mves
            ref_units = Order.objects.filter(instruction=MoveType.CONVOY)\
                .values_list('reference_unit',flat=True)

            # filter to just convoy units
            return self.get_queryset().filter(moves).filter(models.Q(order_reference__unit__in = ref_units))
        else:
            raise TypeError('Type should be Turn')
        
    def grab_all_non_cvy_mve_orders(self,turn,room):
        from room.models.turn import Turn
        from room.models.outcome import Outcome
        from room.models.room import Room
        if isinstance(turn,Turn) and isinstance(room,Room):
            cvy_mves = self.grab_all_cvy_mve_orders(turn,room).values_list('order_reference__unit',flat=True)
            all_mve_orders: models.QuerySet[Outcome] = self.grab_all_mve_orders(turn,room)

            return all_mve_orders.exclude(order_reference__unit__in = cvy_mves)
        else:
            raise TypeError('Type should be Turn')
        
    def get_outcomes_retreat(self,turn,room):
        from room.models.turn import Turn
        from room.models.outcome import OutcomeType
        from room.models.room import Room
        if isinstance(turn,Turn) and isinstance(room,Room):
            query = models.Q(order_reference__room=room) & models.Q(order_reference__turn=turn) & models.Q(validation=OutcomeType.DISLODGED)
            return self.get_queryset().filter(query)
        else:
            raise TypeError('Type should be Turn')
