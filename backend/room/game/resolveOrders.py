class ResolveOrders():
    # this class resolves all legitamite orders
    # call the class LegitamiseOrders before this!
    def __init__(self,turn) -> None:
        from room.models.order import Turn, Outcome, OutcomeType
        if type(turn) is not Turn: raise TypeError('Type should be Turn')
        self.turn = turn

        # 1 - direct (non-convoyed) attacks cut supports
        for outcome in Outcome.objects.grab_all_mve_orders(self.turn):
            self._cut_support(outcome,direct=1)

        # 2 - DETERMINE CONVOY DISRUPTIONS - may need to be in WHILE
        cut,cutters = 1,[]
        while cut:
            cut = 0

            # 2.1 - First mark units if the convoy fleet would be disrupted
            self._check_disruptions(OutcomeType.MARK,OutcomeType.MAYBE) 
            # 2.2 - Cut supports made by convoyed attacks (not including marked)
            for outcome in Outcome.objects.grab_all_cvy_mve_orders(self.turn):
                if type(outcome) is not Outcome: raise TypeError('outcome should be of type Outcome')
                if outcome.validation != OutcomeType.MAYBE or outcome.pk in cutters:
                    continue
                self._cut_support(outcome)
                cutters.append(outcome.pk)
                cut = 1
            if cut:
                continue
            # 2.3 - Locate definite CVY disruptions - uses already Marked as well as all CVY MVEs
            self._check_disruptions(OutcomeType.VOID,OutcomeType.DISRUPTED) 
            
            for outcome in Outcome.objects.grab_all_cvy_mve_orders(self.turn,add_marked=True):
                if type(outcome) is not Outcome: raise TypeError('outcome should be of type Outcome')
                # 2.4 - VOID SPTs to these Disrupted CVY MVEs
                if outcome.validation == OutcomeType.NO_CONVOY:
                    # grab all SPTs referencing this MVE
                    pass
                elif outcome.validation == OutcomeType.MARK:
                    # cut SPTs for marked MVEs
                    pass
                # 2.5 - ALLOW the other Successful CVY MVEs to CUT SPT




        # 3 - MARK BOUNCERS
        # 4 - MARK SUPPORTS CUT BY DISLODGES
        # 5 - MARK DISLODGEMENTS AND UNBOUNCE ALL MOVES THAT LEAD TO DISLODGING UNITS


        
    # if MVE attacks SPT unit cut it
    def _cut_support(self,outcome,direct=0):
        from room.models.order import Outcome, MoveType, OutcomeType
        if type(outcome) is not Outcome: raise TypeError('outcome should be of type Outcome')
        # don't cut for convoy moves if direct
        if direct and len(Outcome.objects.grab_convoy_orders_for_order(self.turn,outcome.order_reference)) > 0: return
        support_to_cut = Outcome.objects.grab_order_current_location(outcome.order_reference.target_location,self.turn).first()
        # could be none i.e. no order, and check if it is support
        if type(support_to_cut) is Outcome and support_to_cut.validation != OutcomeType.CUT and \
                support_to_cut.validation != OutcomeType.VOID and \
                support_to_cut.order_reference.instruction == MoveType.SUPPORT:
            if (# EXCEPTION A: CANNOT CUT SUPPORT YOU YOURSELF ARE GIVING
                    support_to_cut.order_reference.target_unit.owner != \
                    outcome.order_reference.target_unit.owner) and \
                    (# EXCEPTION B: CANNOT CUT SUPPORT FOR A MOVE AGAINST YOUR LOCATION
                    support_to_cut.order_reference.reference_unit_new_location != \
                    outcome.order_reference.current_location
                    ) and \
                    ((# EXCEPTION C: OR SUPPORT FOR A MOVE (IF CONVOYED) FOR OR AGAINST ANY CONVOYING FLEET
                    # p.g. 17 for reference to diagram of this
                    len(Outcome.objects.grab_order_current_location(turn=self.turn, location=
                    support_to_cut.order_reference.reference_unit_new_location)\
                        .filter(order_reference__instruction=MoveType.CONVOY)) == 0) or \
                    (# EXCEPTION TO EXCEPTION C: IF THERE IS A ALTERNATIVE CONVOY ROUTE      
                    Outcome.objects.is_alternative_convoy_route(self.turn,outcome.order_reference,
                    support_to_cut.order_reference.reference_unit_new_location))): 
                # support is cut
                support_to_cut.validation = OutcomeType.CUT
                support_to_cut.save()

    def _check_disruptions(self,mve_order_result,cvy_order_result):
        pass




    # NOTES

    #need to check situations for:
    # disruptions - to convoy
    # -> check paradox - infinite loop?


    # unit bounce - 2 vs 2
    # handle these bounced units    

    # cut support
    # remove units of no affect i.e out of combat
    # unbounce units now at 2 vs 1


    # needs some sort of dfs to work out end of trees
    # i.e. which locations can be resolved easily

    # or 

    # do the ones that can be resolved instantly
    # keep going until all are done (iterative)
    # remove from dict as you go?


    # the ones that can be resolved instantly are ones that don't depend on outside sources
    

    # orrr we do a first pass, only looking at indiviual tiles?

