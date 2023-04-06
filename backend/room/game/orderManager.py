from django.db import models

class OrderManager(models.Manager):
    def validate_order_table(self,turn):
        self.legitamise_orders(turn)
        self.calculate_moves()
        self.evaluate_calulations()
        self.perform_operations()

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
        from room.models.locations import Next_to
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
            if type(outcome) is Outcome:
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
    def calculate_moves(self):
        # move/support
        # each location added to list and tallied
        pass

    # evalulate tallies -> put in table?
    def evaluate_calulations(self):
        # for each calculation evaluate
        # those that fail, order cancels
        pass

    # Move Units
    def perform_operations(self):
        from room.models.order import Outcome
        for successful_outcome in Outcome.objects.filter(validation=True):
            successful_outcome.order_reference.target_unit.move(successful_outcome.order_reference)
