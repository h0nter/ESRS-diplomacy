from django.db import models


class OrderManager(models.Manager):
    def validate_order_table(self,turn):
        self.legitamise_orders(turn)
        self.evaluate_orders(turn)
        self.perform_move_operations(turn)

    # should be static but how to reference inside
    # also don't know where to put this
    def convoy_dfs(self, node, target, graph, visited=set()):
        visited.add(node)
        if node == target:
            return True
        for child in graph[node]:
            if child not in visited:  # Check whether the node is visited or not
                result = self.convoy_dfs(child, target, graph, visited)  # Call the dfs recursively
                
                if result is True:
                    return True
                
        return False

    # remove orders that are theoritcally impossible
    def legitamise_orders(self,turn):
        from room.models.locations import Next_to, Location
        from room.models.order import Order,Outcome
        all_moves_requiring_convoys = []
        for order in Order.objects.filter(turn=turn):
            current_outcome = Outcome.objects.create(order_reference=order,validation=True)
            # check current_location is same as actual
            if(order.current_location == order.target_unit.location):
                # check moves
                if(order.instruction == 'MVE'):
                    # if not valid
                    if(not order.target_unit.validate_move(order)):
                        current_outcome.validation = False
                    else:
                        # valid and needs convoy
                        if(order.current_location.is_coast and order.target_location.is_coast):
                            next_to = Next_to.objects.filter(location=order.current_location)\
                                        .filter(next_to=order.target_location)
                            if(len(next_to) != 1):
                                all_moves_requiring_convoys.append(current_outcome)
                # check supports
                elif(order.instruction == 'SPT'):
                    # if not valid
                    if(not order.target_unit.validate_support(order,turn)):
                        current_outcome.validation = False
                # check convoy
                elif(order.instruction == 'CVY'):
                    # if not valid
                    if(not order.target_unit.validate_convoy(order,turn) or not order.target_unit.can_float):
                        current_outcome.validation = False
                # Hold auto pass
                else:
                    pass
            else:
                current_outcome.validation = False

        # check convoys can actually happen, if not invalidate all involved
        # do dfs convoy here
        for outcome in all_moves_requiring_convoys:
            if type(outcome) is Outcome and type(outcome.order_reference.target_location) is Location:
                # get convoys relating to move
                related_convoys = Outcome.objects.filter(validation=True)\
                                    .filter(order_reference__turn=turn)\
                                    .filter(order_reference__instruction='CVY')\
                                    .filter(order_reference__reference_unit=outcome.order_reference.target_unit)
                graph = {}
                # add current and last locations
                graph[outcome.order_reference.current_location.pk] = \
                        Next_to.objects.filter(location=outcome.order_reference.current_location).values_list('pk',flat=True)
                graph[outcome.order_reference.target_location.pk] = \
                        Next_to.objects.filter(location=outcome.order_reference.target_location).values_list('pk',flat=True)
                # add convoy locations
                for convoy in related_convoys:
                    # create a graph of pks, similar to '1':['2','3','4']
                    graph[convoy.order_reference.current_location.pk] = \
                        Next_to.objects.filter(location=convoy.order_reference.current_location).values_list('pk',flat=True)
                
                if(not self.convoy_dfs(outcome.order_reference.current_location.pk,
                                       outcome.order_reference.target_location.pk,graph)):
                    #if convoy didn't work
                    outcome.validation = False
                    for convoy in related_convoys:
                        convoy.validation = False

    # calculate tallies 
    def calculate_moves(self,turn):
        # move/support
        # each location added to list and tallied
        from locationResolver import LocationResolver, SituationResolver, ResolverList
        from room.models.locations import Location
        from room.models.order import Outcome
        resolverList: ResolverList = ResolverList()

        for legit_order in Outcome.objects.filter(validation=True).filter(order_reference__turn=turn):
            
            resolverList.add_order_locations(legit_order)
            # shorten names
            current_location = legit_order.order_reference.current_location
            target_location = legit_order.order_reference.target_location
            reference_unit_current_location = legit_order.order_reference.reference_unit_current_location
            reference_unit_new_location = legit_order.order_reference.reference_unit_new_location
            #get resolver_id for one as it same for the rest
            resolver_id = resolverList.get_situation_id_by_loc_name(current_location.name)
            location = resolverList.list[resolver_id].locationResolvers

            # defending - current location
            location[current_location.name].add_to_defence(legit_order.order_reference)
            # is the current unit in location
            location[current_location.name].current_unit_order = legit_order.order_reference

            #SPT
            if(legit_order.order_reference.instruction == 'SPT' and reference_unit_current_location):
                if(reference_unit_new_location is None ):
                    # supporting defending unit - this could be a HLD OR CVY
                    location[reference_unit_current_location.name].add_to_defence(legit_order.order_reference)
                elif(reference_unit_new_location and legit_order.order_reference.reference_unit):
                    # supporting a MVE
                    location[reference_unit_new_location.name].add_to_attacking(legit_order.order_reference.reference_unit,legit_order.order_reference)
            #MVE
            elif(legit_order.order_reference.instruction == 'MVE' and target_location):
                location[target_location.name].add_to_attacking(legit_order.order_reference.target_unit,legit_order.order_reference)
                location[current_location.name].current_unit_moved = True
            else:
                # 'HLD' or 'CVY' don't affect other moves already covered with defence
                pass

        return resolverList

    def evaluate_orders(self,turn):
        from locationResolver import LocationResolver, SituationResolver, ResolverList
        resolverList: ResolverList = self.calculate_moves(turn)
        # for each calculation evaluate
        # those that fail, order cancels

        # change location resolver to be situation resolver
        # can then resolve each situation as separate problems linearly
        for situation in resolverList.list:
            # for each sitatution there is a start point, we find the start pt we can resolve everything
            locations = situation.locationResolvers

            if len(locations) == 1:
                #hold unrelated to others passes
                pass
            if len(locations) == 2:
                #length of 2
                for name,location in locations.items():
                    if location.get_attacking_amount == 0:
                        # nothing attacking location so related order all good
                        pass

            else:
                #all other lengths

            # needs some sort of dfs to work out end of trees
            # i.e. which locations can be resolved easily

            # or 

            # do the ones that can be resolved instantly
            # keep going until all are done (iterative)
            # remove from dict as you go?


            # the ones that can be resolved instantly are ones that don't depend on outside sources
            

            # orrr we do a first pass, only looking at indiviual tiles?

            pass

    # Move Units
    def perform_move_operations(self,turn):
        from room.models.order import Outcome
        for successful_outcome in Outcome.objects.filter(validation=True).filter(order_reference__turn=turn):
            successful_outcome.order_reference.target_unit.move(successful_outcome.order_reference.target_location)
