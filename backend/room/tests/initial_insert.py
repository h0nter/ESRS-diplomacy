from ..models  import tables


class InitialInsert:
    # a finish sign decorator
    def stamp(func):
        def wrap(cls):
            func(cls)
            print('function '+func.__name__+' completed')
        return wrap
        
    @classmethod
    def all_insert(cls):
        cls.insertCountry()
        cls.insertLocation()
        cls.insertNext_to()
        cls.insertUnit()
        cls.insertTurn()
        cls.insertOrder()
    
    @classmethod
    # @stamp
    def insertCountry(cls):
        country = tables.Country(name="country A")
        country.save()
        
    @classmethod
    # @stamp
    def insertLocation(cls):
        location = tables.Location(name="first location")
        location.save()
        location = tables.Location(name="second location")
        location.save()
    
    @classmethod
    # @stamp
    def insertNext_to(cls):
        locations = tables.Location.objects.all()
        next_to = tables.Next_to(location=locations[0], next_to=locations[1])
        next_to.save()

    
    @classmethod
    # @stamp
    def insertUnit(cls):
        owner = tables.Country.objects.get(name="country A")
        location = tables.Location.objects.get(name="first location")
        unit = tables.Unit(owner=owner, location=location)
        unit.save()
        
    @classmethod
    # @stamp
    def insertTurn(cls):
        turn = tables.Turn(year=1994)
        turn.save()

    @classmethod
    # @stamp
    def insertOrder(cls):
        instruction = 'MVE'
        turn = tables.Turn.objects.get(year=1994)
        target_unit = tables.Unit.objects.get(pk=1)
        current_location = tables.Location.objects.get(pk=1)
        target_location = tables.Location.objects.get(pk=2)
        order = tables.Order(instruction=instruction, turn=turn, target_unit=target_unit, current_location=current_location, target_location=target_location)
        order.save()