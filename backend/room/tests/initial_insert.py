from room.models.tables  import *


class InitialInsert:
    # a finish sign decorator
    def stamp(func):
        def wrap(cls):
            func(cls)
            print('function '+func.__name__+' completed')
        return wrap
        
    @classmethod
    def all_insert(cls):
        cls.insertMap()
        cls.insertCountry()
        cls.insertLocation()
        cls.insertNext_to()
        cls.insertUnit()
        cls.insertTurn()
        cls.insertOrder()

    @classmethod
    # @stamp
    def insertMap(cls):
        map = Map(name="A magic map", max_countries=7)
        map.save()
    
    @classmethod
    # @stamp
    def insertCountry(cls):
        map = Map.objects.first()
        country = Country(name="country A", map=map,colour='red')
        country.save()
        
    @classmethod
    # @stamp
    def insertLocation(cls):
        map = Map.objects.first()
        location = Location(name="first location",map=map)
        location.save()
        location = Location(name="second location",map=map)
        location.save()
    
    @classmethod
    # @stamp
    def insertNext_to(cls):
        locations = Location.objects.all()
        next_to = Next_to(location=locations[0], next_to=locations[1])
        next_to.save()

    
    @classmethod
    # @stamp
    def insertUnit(cls):
        owner = Country.objects.get(name="country A")
        location = Location.objects.get(name="first location")
        unit = Unit(owner=owner, location=location)
        unit.save()
        
    @classmethod
    # @stamp
    def insertTurn(cls):
        turn = Turn(year=1994)
        turn.save()

    @classmethod
    # @stamp
    def insertOrder(cls):
        instruction = 'MVE'
        turn = Turn.objects.get(year=1994)
        target_unit = Unit.objects.first()
        current_location = Location.objects.all()[0]
        target_location = Location.objects.all()[1]
        order = Order(instruction=instruction, turn=turn, target_unit=target_unit, current_location=current_location, target_location=target_location)
        order.save()