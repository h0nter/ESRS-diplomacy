from django.db import models
from room.models.locations import Country, Location

class Unit(models.Model):
    # Don't want to delete previous location if Unit moves
    
    owner = models.ForeignKey(Country,on_delete=models.CASCADE)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    can_float = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Units'
    def __str__(self):
        return str(self.pk)

    def move(self,location):
        if(type(location) is Location):
            #thisUnit = Unit.objects.get(pk=self.pk)
            self.location = location
            self.save()
        else:
            raise TypeError('Type should be Location')
        
    def check_move_next_to(self,order) -> bool:
        from room.models.locations import Next_to
        next_to = Next_to.objects.filter(location=order.current_location)\
            .filter(next_to=order.target_location)
        if(len(next_to) == 1):
            return True
        else:
            return False

    def validate_move(self,order) -> bool:
        if(order.target_unit.can_float):
            #Fleet
            if(( order.current_location.is_sea or order.current_location.is_coast) and
                ( order.target_location.is_sea or order.target_location.is_coast)):
                return self.check_move_next_to(order)
            else:
                return False
        else:
            # Army
            if(order.current_location.is_coast and order.target_location.is_coast):
                # coast to coast - convoy assist
                # theoritically true as long as convoys ok
                return True
            elif((not order.current_location.is_sea or order.current_location.is_coast) and
            (not order.target_location.is_sea or order.target_location.is_coast)):
                # land to land - move
                # complicated due to constantinopale - sea and coast at same time..
                return self.check_move_next_to(order)
            else:
                return False

    def check_support_targets_correctly(self,order,turn) -> bool:   
        # check adjacent
        from room.models.locations import Next_to
        next_to = Next_to.objects.filter(location=order.current_location)\
            .filter(next_to=order.reference_unit_new_location)
        if(len(next_to) == 1):
            # able to support check if support possible
            # check referenced Unit is making same Order
            from room.models.order import Order
            support_unit_order = Order.objects.filter(turn=turn)\
                .filter(target_unit=order.reference_unit)\
                .filter(current_location=order.reference_unit_current_location)\
                .filter(target_location=order.reference_unit_new_location)\
                .filter(instruction='MVE')
            if(len(support_unit_order) == 1):
                return True
        return False
            

    def validate_support(self,order,turn) -> bool:
        from room.models.locations import Location,Next_to
        if(order.target_unit.can_float):
            #Fleet
            if((order.current_location.is_sea or order.current_location.is_coast) and 
                type(order.reference_unit_new_location) is Location):
                # should be able to move where it is supporting
                if( order.reference_unit_new_location.is_sea or order.reference_unit_new_location.is_coast):
                    return self.check_support_targets_correctly(order,turn)
            return False
        else:
            #Army
            if((not order.current_location.is_sea or order.current_location.is_coast) and 
           type(order.reference_unit_new_location) is Location):
                # should be able to move where it is supporting
                if(not order.reference_unit_new_location.is_sea or order.reference_unit_new_location.is_coast):
                    return self.check_support_targets_correctly(order,turn)
            return False

    def validate_convoy(self,order,turn) -> bool:
        # validate theoretical convoy
        # has to be in sea
        from room.models.order import Order
        if(order.current_location.is_sea):
            convoy_unit_order = Order.objects.filter(turn=turn)\
                        .filter(target_unit=order.reference_unit)\
                        .filter(current_location=order.reference_unit_current_location)\
                        .filter(target_location=order.reference_unit_new_location)\
                        .filter(instruction='MVE')
            if(len(convoy_unit_order) == 1):
                return True
        return False
