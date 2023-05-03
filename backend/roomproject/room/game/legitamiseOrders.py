class LegitamiseOrders():
    # this class takes the indiviually valid orders
    # and filters the non-valid overall orders
    # e.g. SPT or CVY references a null unit
    # or CVY not valid etc.
    def __init__(self,turn) -> None:
        from room.models.order import Turn
        if type(turn) is Turn:
            self._legitamise_orders(turn)
        else:
            raise TypeError('Type should be Turn')

    # private as only needed for legitamising the convoy order
    def _convoy_dfs(self, node, target, graph, visited=set()):
        visited.add(node)
        if node == target:
            return True
        elif node in graph:
            for child in graph[node]:
                if child not in visited:  # Check whether the node is visited or not
                    result = self._convoy_dfs(child, target, graph, visited)  # Call the dfs recursively
                    
                    if result is True:
                        return True
                
        return False

    # remove orders that are theoritcally impossible
    def _legitamise_orders(self,turn):
        from room.models.locations import Next_to, Location
        from room.models.order import Order,Outcome, MoveType, OutcomeType
        all_moves_requiring_convoys = []
        for order in Order.objects.filter(turn=turn):
            if type(order) is not Order: continue
            current_outcome = Outcome.objects.create(order_reference=order)
            current_outcome.save() # save init
            if order.instruction == MoveType.HOLD:
                #auto pass, checks done when submitted to Order originally
                pass
            elif order.instruction == MoveType.MOVE:
                #auto pass, checks done when submitted to Order originally
                pass
            elif order.instruction == MoveType.SUPPORT:
                reference_unit_order = Order.objects.filter(turn=turn)\
                .filter(target_unit=order.reference_unit)\
                .filter(current_location=order.reference_unit_current_location)\
                .filter(target_location=order.reference_unit_new_location)\
                .filter(instruction=MoveType.MOVE)
                if(len(reference_unit_order) == 1):
                    # check move exists - it does so all good
                    pass
                else:
                    # spt void but unit acts like hld
                    current_outcome.validation = OutcomeType.VOID
                    current_outcome.save()
            elif order.instruction == MoveType.CONVOY:
                reference_unit_order = Order.objects.filter(turn=turn)\
                .filter(target_unit=order.reference_unit)\
                .filter(current_location=order.reference_unit_current_location)\
                .filter(target_location=order.reference_unit_new_location)\
                .filter(instruction=MoveType.MOVE)
                if(len(reference_unit_order) == 1):
                    # check move exists - it does so all good
                    # can add to defending here but need to check overall convoy
                    all_moves_requiring_convoys.append(reference_unit_order.first())
                else:
                    # cvy void bout unit acts like hld
                    current_outcome.validation = OutcomeType.VOID
                    current_outcome.save()

        #remove duplicate mve orders
        all_moves_requiring_convoys = list(dict.fromkeys(all_moves_requiring_convoys))
        # check convoys can actually happen, if not invalidate all involved
        # do dfs convoy here
        for outcome in all_moves_requiring_convoys:
            if type(outcome) is Outcome and type(outcome.order_reference.target_location) is Location:
                # get convoys relating to move
                related_convoys = Outcome.objects.filter(validation=OutcomeType.MAYBE)\
                                    .filter(order_reference__turn=turn)\
                                    .filter(order_reference__instruction=MoveType.CONVOY)\
                                    .filter(order_reference__reference_unit=outcome.order_reference.target_unit)
                graph = {}
                # add current and last locations
                graph[outcome.order_reference.current_location.pk] = \
                        list(Next_to.objects.filter(location=outcome.order_reference.current_location).values_list('next_to__pk',flat=True))
                graph[outcome.order_reference.target_location.pk] = \
                        list(Next_to.objects.filter(location=outcome.order_reference.target_location).values_list('next_to__pk',flat=True))
                # add convoy locations
                for convoy in related_convoys:
                    # create a graph of pks, similar to '1':['2','3','4']
                    graph[convoy.order_reference.current_location.pk] = \
                        list(Next_to.objects.filter(location=convoy.order_reference.current_location).values_list('next_to__pk',flat=True))
                
                if(not self._convoy_dfs(outcome.order_reference.current_location.pk,
                                       outcome.order_reference.target_location.pk,graph)):
                    #if convoy didn't work
                    outcome.validation = OutcomeType.VOID
                    outcome.save()
                    for convoy in related_convoys:
                        convoy.validation = OutcomeType.VOID
                        convoy.save()
                else:
                    #convoy success, add mve to attacking
                    pass