# from abc import ABC, abstractmethod
# from room.models.tables import Order, Unit, Location, Country


# # design pattern of factor method
# class AbstractUnit(ABC):
#     # constructe with a order model
#     def __init__(self, order) -> None:
#         self.order:Order = order
#         self.unit = self.order.target_unit
#         self.can_float = self.unit.can_float
#         self.instruction = self.order.instruction
    
#     # announce the methods and will be implement in child class
#     @abstractmethod
#     def move(self):
#         # print('unit ')
#         # print(Unit.objects.filter(pk=self.unit.pk).first().location)
#         print('location')
#         print(self.order.target_location)
#         # Unit.objects.filter(pk=self.unit.pk).update(location=self.order.target_location)
#         # print('after')
#         # print(Unit.objects.filter(pk=self.unit.pk).first().location)
#         # self.unit = Unit.objects.filter(pk=self.unit.pk).first()

#         self.unit.location = self.order.target_location
#         self.unit.save()
#         print(self.unit.location)

#     @abstractmethod
#     def support(self):
#         pass
