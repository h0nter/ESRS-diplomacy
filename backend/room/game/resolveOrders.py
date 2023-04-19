class ResolveOrders():
    def __init__(self,turn) -> None:
        from room.models.order import Turn
        if type(turn) is Turn:
            pass
        else:
            raise TypeError('Type should be Turn')
        

    # if MVE attacks SPT unit cut it
    def _cut_supports_direct(self,turn):
        from room.models.order import Outcome, MoveType
        for outcome in Outcome.objects.grab_all_mve_orders(turn):
            if type(outcome) is not Outcome: continue
            support_to_cut = Outcome.objects.grab_order_current_location(outcome.order_reference.target_location,turn).first()
            # could be none i.e. no order, and check if it is support
            if type(support_to_cut) is Outcome and \
                support_to_cut.order_reference.instruction == MoveType.SUPPORT:
                if (# EXCEPTION A: CANNOT CUT SUPPORT YOU YOURSELF ARE GIVING
                    support_to_cut.order_reference.target_unit.owner != \
                    outcome.order_reference.target_unit.owner) and \
                    (# EXCEPTION B: CANNOT CUT SUPPORT FOR A MOVE AGAINST YOUR LOCATION
                    support_to_cut.order_reference.reference_unit_new_location != \
                    outcome.order_reference.current_location
                    ):
                    # EXCEPTION C: OR SUPPORT FOR A MOVE (IF CONVOYED) FOR OR AGAINST ANY CONVOYING FLEET
                    # p.g. 17 for reference to diagram of this
                    # EXCEPTION TO EXCEPTION C: IF THERE IS A ALTERNATIVE CONVOY ROUTE


    def evaluate_orders(self,turn):
        from locationResolver import LocationResolver, SituationResolver, ResolverList
        #resolverList: ResolverList = self.calculate_moves(turn)
        # for each calculation evaluate
        # those that fail, order cancels
        #resolverList = []
        # change location resolver to be situation resolver
        # can then resolve each situation as separate problems linearly
        #for situation in resolverList.list:
            # for each sitatution there is a start point, we find the start pt we can resolve everything
            #locations = situation.locationResolvers

            # 3. let direct (non-convoyed) attacks cut supports

            # STEPS 4 AND 5. DETERMINE CONVOY DISRUPTIONS
            # STEP 4. CUT SUPPORTS MADE BY (non-maybe) CONVOYED ATTACKS
            # STEP 5. LOCATE NOW-DEFINITE CONVOY DISRUPTIONS, VOID SUPPORTS
            #       THESE CONVOYERS WERE GIVEN, AND ALLOW CONVOYING UNITS TO CUT SUPPORT

            # STEPS 6-8. MARK BOUNCERS
            # STEP 9. MARK SUPPORTS CUT BY DISLODGES
            # STEP 10. MARK DISLODGEMENTS AND UNBOUNCE ALL MOVES THAT LEAD TO DISLODGING UNITS


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

        pass
