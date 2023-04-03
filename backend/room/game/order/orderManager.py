from django.db import models
from backend.room.models.units import Army,Fleet
from room.models.tables import Turn,Order,Outcome,Next_to


class OrderManager(models.Manager):
    def validate_order_table(self,turn:Turn):
        self.legitamise_orders(turn)
        self.calculate_moves()
        self.evaluate_calulations()
        self.perform_operations()
        pass

    # remove orders that are theoritcally impossible
    def legitamise_orders(self,turn:Turn):
        # current?? - input turn number somehow
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
                    if(not order.target_unit.validate_convoy(order,turn) or type(order.target_unit) is not Fleet):
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


        pass

    # calculate tallies 
    def calculate_moves(self):
        # move/support
        # each location added to list and tallied
        pass

    # evalulate tallies -> put in table?
    def evaluate_calulations(self) :
        # for each calculation evaluate
        # those that fail, order cancels
        pass

    # Move Units
    def perform_operations(self):
        for successful_outcome in Outcome.objects.filter(validation=True):
            successful_outcome.order_reference.target_unit.move(successful_outcome.order_reference)
        pass