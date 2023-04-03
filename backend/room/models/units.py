from room.models.tables import Unit,Order,Turn,Location,Next_to

# Moving an actual Unit is done via the Parent Class Unit
# Calling move(order), this changes the location in the database
class Army(Unit):
    def validate_move(self,order:Order) -> bool:
        if((not order.current_location.is_sea or order.current_location.is_coast) and
           (not order.target_location.is_sea or order.target_location.is_coast)):
            # land to land - move
            # complicated due to constantinopale - sea and coast at same time..
            next_to = Next_to.objects.filter(location=order.current_location)\
                .filter(next_to=order.target_location)
            if(len(next_to) == 1):
                return True
            else:
                return False
        elif(order.current_location.is_coast and order.target_location.is_coast):
            # coast to coast - convoy assist
            # theoritically true as long as convoys ok
            return True
        else:
            return False
    
    def validate_support(self,order:Order,turn:Turn) -> bool:
        if((not order.current_location.is_sea or order.current_location.is_coast) and 
           type(order.reference_unit_new_location) is Location):
               # should be able to move where it is supporting
            if(not order.reference_unit_new_location.is_sea or order.reference_unit_new_location.is_coast):
                # check adjacent
                next_to = Next_to.objects.filter(location=order.current_location)\
                    .filter(next_to=order.reference_unit_new_location)
                if(len(next_to) == 1):
                    # able to support check if support possible
                    # check referenced Unit is making same Order
                    support_unit_order = Order.objects.filter(turn=turn)\
                        .filter(target_unit=order.target_unit)\
                        .filter(current_location=order.reference_unit_current_location)\
                        .filter(target_location=order.reference_unit_new_location)\
                        .filter(instruction='MVE')
                    if(len(support_unit_order) == 1):
                        return True
        return False


class Fleet(Unit):
    def validate_move(self,order:Order) -> bool:
        if(( order.current_location.is_sea or order.current_location.is_coast) and
           ( order.target_location.is_sea or order.target_location.is_coast)):
            # sea to sea, sea to coast, coast to sea, coast to coast
            next_to = Next_to.objects.filter(location=order.current_location).filter(next_to=order.target_location)
            if(len(next_to) == 1):
                return True
        return False

    def validate_support(self,order:Order,turn:Turn) -> bool:
        if((order.current_location.is_sea or order.current_location.is_coast) and 
           type(order.reference_unit_new_location) is Location):
               # should be able to move where it is supporting
            if( order.reference_unit_new_location.is_sea or order.reference_unit_new_location.is_coast):
                # check adjacent
                next_to = Next_to.objects.filter(location=order.current_location)\
                    .filter(next_to=order.reference_unit_new_location)
                if(len(next_to) == 1):
                    # able to support check if support possible
                    # check referenced Unit is making same Order
                    support_unit_order = Order.objects.filter(turn=turn)\
                        .filter(target_unit=order.target_unit)\
                        .filter(current_location=order.reference_unit_current_location)\
                        .filter(target_location=order.reference_unit_new_location)\
                        .filter(instruction='MVE')
                    if(len(support_unit_order) == 1):
                        return True
        return False

    def validate_convoy(self,order:Order,turn:Turn) -> bool:
        # validate theoretical convoy
        # has to be in sea
        if(order.current_location.is_sea):
            convoy_unit_order = Order.objects.filter(turn=turn)\
                        .filter(target_unit=order.target_unit)\
                        .filter(current_location=order.reference_unit_current_location)\
                        .filter(target_location=order.reference_unit_new_location)\
                        .filter(instruction='MVE')
            if(len(convoy_unit_order) == 1):
                        return True
        return False
    #         self.unit = Unit.objects.filter(pk=self.unit.pk).first()
    #         self.unit.location = self.order.target_location
    #         self.unit.save()

    # should be static but how to reference inside
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