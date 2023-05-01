from django.db import models


class ResolveOrders():
    # this class resolves all legitamite orders
    # call the class LegitamiseOrders before this!
    def __init__(self,turn) -> None:
        from room.models.order import Turn, Outcome, OutcomeType, MoveType
        if type(turn) is not Turn: raise TypeError('Type should be Turn')
        self.turn = turn

        # 1 - direct (non-convoyed) attacks cut supports
        for outcome in Outcome.objects.grab_all_mve_orders(self.turn):
            self._cut_support(outcome,direct=1)

        # 2 - DETERMINE CONVOY DISRUPTIONS
        self._determine_convoy_disruptions()

        cut = True
        while cut:
            # 3 - MARK BOUNCERS
            self._bounce()

            # 4 - MARK SUPPORTS CUT BY DISLODGES - this being potentially mves 
            cut = self._cut_supports_from_dislodge()
            
        # 5 - MARK DISLODGEMENTS AND UNBOUNCE ALL MOVES THAT LEAD TO DISLODGING UNITS
        for outcome in Outcome.objects.grab_all_mve_orders(self.turn):
            if type(outcome) is not Outcome: raise TypeError('outcome should be of type Outcome')
            self._determine_dislodgement(outcome)
            outcome_location = outcome.order_reference.target_location
            self._unbounce(outcome_location)

        # Note: 
        # all dislodged units will need to grab move orders from player
        # these then need to be validated
        
    def _determine_convoy_disruptions(self):
        from room.models.order import Outcome, OutcomeType
        cut,cutters = True,[]
        while cut:
            cut = False

            # 2.1 - First mark units if the convoy fleet would be disrupted
            self._check_disruptions(OutcomeType.MARK,OutcomeType.MAYBE) 
            # 2.2 - Cut supports made by convoyed attacks (not including marked)
            for outcome in Outcome.objects.grab_all_cvy_mve_orders(self.turn):
                if type(outcome) is not Outcome: raise TypeError('outcome should be of type Outcome')
                if outcome.validation != OutcomeType.MAYBE or outcome.pk in cutters:
                    continue
                self._cut_support(outcome)
                cutters.append(outcome.pk)
                cut = True
            if cut:
                continue
            # 2.3 - Locate definite CVY disruptions - uses already Marked as well as all CVY MVEs
            self._check_disruptions(OutcomeType.NO_CONVOY,OutcomeType.DISRUPTED) 
            
            for outcome in Outcome.objects.grab_all_cvy_mve_orders(self.turn,add_marked=True):
                if type(outcome) is not Outcome: raise TypeError('outcome should be of type Outcome')
                # 2.4 - VOID SPTs to these Disrupted CVY MVEs
                if outcome.validation == OutcomeType.NO_CONVOY:
                    # grab all SPTs referencing this MVE
                    for support_outcome in Outcome.objects.grab_related_spt_orders(outcome.order_reference,self.turn):
                        if type(support_outcome) is not Outcome: raise TypeError('outcome should be of type Outcome')
                        outcome.validation = OutcomeType.NO_CONVOY
                        outcome.save()
                elif outcome.validation == OutcomeType.MARK:
                    # 2.5 - ALLOW the other Successful CVY MVEs to CUT SPT
                    # cut SPTs for marked MVEs
                    outcome.validation = OutcomeType.MAYBE
                    outcome.save()
                    self._cut_support(outcome)
                    cutters.append(outcome.pk)
                    cut = True

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
        # determines convoy disruptions
        from room.models.order import Outcome, Next_to
        for outcome in Outcome.objects.grab_all_cvy_mve_orders(self.turn,add_marked=True):
            if type(outcome) is not Outcome: raise TypeError('outcome should be of type Outcome')
            # grab unit destination order
            order_at_start = outcome.order_reference
            order_at_dest = Outcome.objects.grab_order_current_location(outcome.order_reference.target_location,self.turn).first()

            # for each convoying unit
            for convoy in Outcome.objects.grab_convoy_orders_for_order(self.turn,outcome.order_reference):
                if type(convoy) is not Outcome: raise TypeError('convoy should be of type Outcome')
                # check if being attacked
                attack_orders = Outcome.objects.grab_mve_attacking_orders(convoy.order_reference.current_location,self.turn)
                defence_orders = Outcome.objects.grab_all_defence_orders(convoy.order_reference.current_location,self.turn)
                if len(attack_orders) == 0:
                    #convoy not under attack
                    continue

                # Paradox Detection #1 - diagram 30
                # A convoyed Army doesn’t cut the support of a unit supporting
                # an attack against one of the Fleets necessary for the Army to convoy. 
                paradox = False
                if type(order_at_dest) is Outcome:
                    if order_at_dest.order_reference.reference_unit_new_location == \
                        convoy.order_reference.current_location:
                        paradox = True
                
                # check convoy can withstand attack and there is no paradox
                if len(defence_orders) >= len(attack_orders) and not paradox:
                    continue

                # check destination is not attacking or supporting an attack against convoy
                if type(order_at_dest) is Outcome:
                    if len(attack_orders) >= 2 and not paradox:
                        if order_at_dest not in attack_orders:
                            continue


                # Paradox Detection #2 - Can convoyed unit use land route to cut support necessary to attack convoy
                # if mve is along coast
                paradox = False
                next_to = Next_to.objects.filter(location=order_at_start.current_location)\
                            .filter(next_to=order_at_start.target_location)
                if type(order_at_dest) is Outcome:
                    if len(next_to) == 1 and \
                        order_at_dest.order_reference.reference_unit_new_location == \
                            convoy.order_reference.current_location:
                        paradox = True

                # Setting the result if there is no convoy paths left, and
                #   1) there is no land route (or there is a paradox through the land route)
                #   or 2) the unit specified 'VIA' and doesn't want to try the land route (4.A.3) - doesn't apply
                if(Outcome.objects.is_alternative_convoy_route(
                    self.turn,outcome,convoy.order_reference.current_location)) and \
                   (paradox or not len(next_to) == 1):
                    outcome.validation = mve_order_result
                    outcome.save()


                # Setting the result for a would-be dislodged fleet
                convoy.validation = cvy_order_result
                convoy.save()

    def _bounce(self):
        from room.models.order import Outcome, OutcomeType, MoveType
        # marks all units that can't get where they are going as bounced
        # loops to handle bounce chains
        bounced = 1
        while bounced:
            bounced = 0

             # 3.1 - VOID (non-convoyed) PLACE-SWAP BOUNCERS
            mve_outcomes = Outcome.objects.grab_all_non_cvy_mve_orders(self.turn)
            if type(mve_outcomes) is models.QuerySet[Outcome]:
                # only do for loop if there are moves involving no cvys
                for mve_outcome in mve_outcomes:
                    outcome_at_destination = Outcome.objects.grab_defender_current_location(
                        mve_outcome.order_reference.target_location,self.turn).first()
                    print(outcome_at_destination)
                    # no outcome at destination, skip as no bounce
                    if type(outcome_at_destination) is not Outcome: continue
                        #raise TypeError('outcome_at_destination should be Outcome')
                    # order not evaled yet and of type move i.e also attacking us - i.e. swapping
                    if outcome_at_destination.validation == OutcomeType.MAYBE and \
                        outcome_at_destination.order_reference.instruction == MoveType.MOVE:
                        # if looking at each other boing
                        # check move is not convoying and they are both looking at each other
                        # trading_places = 
                        #     outcome_at_destination in mve_outcomes and \
                        #     mve_outcome.order_reference.current_location == outcome_at_destination.order_reference.target_location and \
                        #     outcome_at_destination.order_reference.current_location == mve_outcome.order_reference.target_location
                        # if same owner boing
                        same_owner = mve_outcome.order_reference.target_unit.owner == \
                            outcome_at_destination.order_reference.target_unit.owner
                        attacking_mve_outcome = len(Outcome.objects.grab_attacking_strength_of_order(mve_outcome.order_reference,self.turn))
                        defending_mve_outcome = len(Outcome.objects.grab_all_defence_orders(mve_outcome.order_reference.current_location,self.turn))
                        attacking_outcome_at_destination = len(Outcome.objects.grab_attacking_strength_of_order(outcome_at_destination.order_reference,self.turn))
                        defending_outcome_at_destination = len(Outcome.objects.grab_all_defence_orders(outcome_at_destination.order_reference.current_location,self.turn))
                        # mve_outcome <= outcome_at_dest
                        if same_owner or attacking_mve_outcome >= defending_mve_outcome:
                            # mve_outcome failed - bounced#
                            print('mve_outcome <= outcome_at_dest',attacking_mve_outcome,defending_mve_outcome,same_owner)
                            mve_outcome.validation = OutcomeType.BOUNCE
                            mve_outcome.save()
                        # outcome_at_dest >= mve_outcome
                        if same_owner or attacking_outcome_at_destination >= defending_outcome_at_destination:
                            print('outcome_at_dest >= mve_outcome',attacking_outcome_at_destination,defending_outcome_at_destination,same_owner)
                            outcome_at_destination.validation = OutcomeType.BOUNCE
                            outcome_at_destination.save()

                        for mve_outcome_support in Outcome.objects.grab_related_spt_orders(mve_outcome.order_reference,self.turn):
                            if type(mve_outcome_support) is not Outcome: raise TypeError('outcome_at_destination should be Outcome')
                            mve_outcome_support.validation = OutcomeType.BOUNCE
                            mve_outcome_support.save()

                        for outcome_at_destination_support in Outcome.objects.grab_related_spt_orders(outcome_at_destination.order_reference,self.turn):
                            if type(outcome_at_destination_support) is not Outcome: raise TypeError('outcome_at_destination should be Outcome')
                            outcome_at_destination_support.validation = OutcomeType.BOUNCE
                            outcome_at_destination_support.save()
                        bounced = 1
                if bounced:
                    continue
                # No (more) swap-bouncers

            # 3.2 - MARK OUTGUNNED BOUNCERS
            for outcome in Outcome.objects.grab_all_mve_orders(self.turn):
                if type(outcome) is not Outcome: raise TypeError('outcome should be Outcome')
                # check target_location has unit
                if len(Outcome.objects.grab_order_current_location(
                    outcome.order_reference.target_location,self.turn)) != 1:
                    continue
                # check defence > attack
                attacking_outcome = len(Outcome.objects.grab_attacking_strength_of_order(outcome.order_reference,self.turn))
                defending_target_location = len(Outcome.objects.grab_all_defence_orders(outcome.order_reference.target_location,self.turn))
                if attacking_outcome <= defending_target_location:
                    # mark attack bounced
                    outcome.validation = OutcomeType.BOUNCE
                    outcome.save()
                    bounced = 1
                # what about the multiple attackers! - this might not be needed...
                # other_attacks on same location see if current order bounces with them
                other_attacks = Outcome.objects.grab_mve_attacking_orders(outcome.order_reference.target_location,self.turn)\
                    .exclude(order_reference__target_unit=outcome.order_reference.target_unit)
                for other_attack in other_attacks:
                    if type(other_attack) is not Outcome: raise TypeError('other_attack should be Outcome')
                    attacking_other_attack = len(Outcome.objects.grab_attacking_strength_of_order(other_attack.order_reference,self.turn))
                    if attacking_outcome <= attacking_other_attack:
                        # attacking outcome will also bounce
                        outcome.validation = OutcomeType.BOUNCE
                        outcome.save()
                        bounced = 1
            if bounced:
                continue

            # 3.3 - MARK SELF-DISLODGE BOUNCERS
            for outcome in Outcome.objects.grab_all_mve_orders(self.turn):
                if type(outcome) is not Outcome: raise TypeError('outcome should be Outcome')
                order_at_location = Outcome.objects.grab_order_current_location(\
                    outcome.order_reference.target_location,self.turn).first()
                # if there is no order at location skip
                if type(order_at_location) is not Outcome: continue
                # if order has same owner 
                if order_at_location.order_reference.target_unit.owner ==\
                    outcome.order_reference.target_unit.owner:
                    # bounce attack
                    outcome.validation = OutcomeType.BOUNCE
                    outcome.save()
                    # bounce spts
                    for outcome_at_destination_support in Outcome.objects.grab_related_spt_orders(outcome.order_reference,self.turn):
                            if type(outcome_at_destination_support) is not Outcome: raise TypeError('outcome_at_destination should be Outcome')
                            outcome_at_destination_support.validation = OutcomeType.BOUNCE
                            outcome_at_destination_support.save()

    def _cut_supports_from_dislodge(self) -> bool:
        from room.models.order import Outcome, OutcomeType, MoveType
        cut = False
        # ones that are marked as bounced -> already evaled
        for outcome in Outcome.objects.grab_all_mve_orders(self.turn):
                if type(outcome) is not Outcome: raise TypeError('outcome should be of type Outcome')
                order_at_target_location = Outcome.objects.grab_order_current_location(
                    outcome.order_reference.target_location,self.turn).first()
                # if there is no order at location skip
                if type(order_at_target_location) is not Outcome: continue
                # if there it is not spt then it cannot be cut
                if order_at_target_location.order_reference.instruction != MoveType.SUPPORT: continue
                # if already been evaluated 
                if order_at_target_location.validation != OutcomeType.MAYBE: continue

                # This next line is the key. Convoyed attacks can dislodge, but even when doing so, they cannot cut
                # supports offered for or against a convoying fleet
                # (They can cut supports directed against the original position of the army, though.)    

                # if cvy attack and spt is directed at cvy fleet: continue
                is_convoy = len(Outcome.objects.grab_all_cvy_mve_orders(self.turn)\
                                .filter(order_reference=outcome.order_reference))==1
                spt_target = Outcome.objects.grab_order_current_location(
                    order_at_target_location.order_reference.reference_unit_new_location,self.turn).first()
                if type(spt_target) is not Outcome: continue
                spt_target_is_convoy = spt_target.order_reference.instruction == MoveType.CONVOY
                if is_convoy and spt_target_is_convoy:
                    continue

                # cut support
                order_at_target_location.validation = OutcomeType.CUT
                order_at_target_location.save()
                cut = True
        return cut
    
    def _determine_dislodgement(self,outcome):
        from room.models.order import Outcome, OutcomeType, MoveType
        if type(outcome) is not Outcome: raise TypeError('outcome should be of type Outcome')
        outcome_location = outcome.order_reference.target_location
        loser = Outcome.objects.grab_order_current_location(outcome_location,self.turn).first()
        # if there is no unit, or unit is already moving don't dislodge it
        if type(loser) is Outcome and loser.order_reference.instruction != MoveType.MOVE:
            loser.validation = OutcomeType.DISLODGED
            loser.save()

            # DOES THIS NEED TO BE DONE?
            # Check for a dislodged swapper (attacker and dislodged units must not be convoyed.)
            # If found, remove the swapper from the combat list of the attacker's space

            # mark support for self-dislodgement as void
            for supporting_unit in Outcome.objects._grab_spt_attacking_orders(
                outcome_location,self.turn).filter(
                order_reference__reference_unit = outcome.order_reference.target_unit):
                if type(supporting_unit) is not Outcome: raise TypeError('outcome should be of type Outcome')
                supporting_unit.validation = OutcomeType.VOID
                supporting_unit.save()

    def _unbounce(self,outcome_location):
        # unbounce any powerful-enough move that can now take the spot being vacated by the dislodger
        from room.models.order import Outcome, OutcomeType, MoveType
        from room.models.locations import Location
        # Detecting if there is only one attack winning at site
        if type(outcome_location) is not Location: raise TypeError('outcome_location should be of type Location')
        highest_attack_mve = Outcome.objects.grab_highest_attacking_mve(outcome_location,self.turn,include_bounce=True)
        #print(outcome_location.name,highest_attack_mve)
        # if still bounce return
        if len(highest_attack_mve) > 1:
            return
        # remove list
        highest_attack_mve = highest_attack_mve[0]
        if type(highest_attack_mve) is not Outcome: raise TypeError('outcome should be of type Outcome')
        # if highest attack still bounce
        if highest_attack_mve.validation == OutcomeType.BOUNCE:
            # pass attack
            highest_attack_mve.validation = OutcomeType.PASS
            highest_attack_mve.save()
        
            #PROBLEM currently difficulty is determining which sites still need resolving        
            # unbounce site highest_attack is on
            next_site = Outcome.objects.grab_mve_attacking_orders(
                highest_attack_mve.order_reference.current_location,self.turn,include_bounce=True)
            if len(next_site) > 1:
                # potentially still needs unbouncing
                self._unbounce(highest_attack_mve.order_reference.current_location)
        return 