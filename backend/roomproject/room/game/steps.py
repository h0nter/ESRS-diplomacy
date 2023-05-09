from room.game.legitamiseOrders import LegitamiseOrders
from room.game.resolveOrders import ResolveOrders
from room.models.room import RoomStatus, Room
from room.models.order import Order, MoveType
from room.models.outcome import Outcome
from room.models.turn import Turn
from room.models.unit import Unit
from room.models.country import Country
from room.models.location import Location
from room.models.location import Map
from room.models.location_owner import LocationOwner
from django.core.management import call_command, base
from django.core.management.commands import loaddata
import json
import datetime
import os

class Step:
    @classmethod
    def __init__(cls, room_id: int):
        cls.room = Room.objects.get(pk=room_id)
        cls.status = cls.room.status
        cls.map_pk = 1 if cls.room.map is None else int(cls.room.map.pk)

        if cls.status == RoomStatus.REGISTERED:  # Formating the room database
            print(cls.status)
            cls.initialize()
            #sets RoomStatus to OPEN

    @classmethod
    def isFinished(cls) -> bool:
        return cls.current_turn.year > 1950
    
    @classmethod
    def initializeDatabase(cls,path):
        #json_files = [pos_json for pos_json in os.listdir(cwd) if pos_json.endswith('.json')]
        json_files = ['map.json','turn.json','country.json','location.json','next_to.json','map_polygon.json']
        # format the room database
        try:
            with open(path + '/room/game/data/loaddata_out.txt', 'w') as file:
                try:
                    for json_file in json_files:
                        file.write(json_file + ': ')
                        call_command(loaddata.Command(), path+'/room/fixtures/'+json_file, stdout=file, verbosity=1)
                        file.write('\n')
                except (IOError, OSError, base.CommandError,Exception) as e:
                    print("Error writing to file {}".format(e))
        except (FileNotFoundError, PermissionError, OSError):
            print("Error opening file")
    
    @classmethod
    def initializeUnits(cls,path):
        try:
            with open(path + '/room/game/data/unit.json','r') as j:
                try:
                    units_all = json.loads(j.read())
                    units = units_all[str(cls.map_pk)]
                    for unit in units:
                        unitModel = Unit(
                            owner=Country.objects.get(pk=unit['unit_owner']),
                            room=cls.room,
                            location=Location.objects.get(pk=unit['unit_location']),
                            can_float=unit['unit_can_float']
                        )
                        unitModel.save()
                except (IOError, OSError,Exception) as e:
                    print("Error writing to file {}".format(e))
        except (FileNotFoundError, PermissionError, OSError):
            print("Error opening file")
        

    @classmethod
    def initializeLocationOwners(cls,path):
        try:
            with open(path+'/room/game/data/location_owner.json','r') as j:
                try:
                    location_owners_all = json.loads(j.read())
                    location_owners = location_owners_all[str(cls.map_pk)]
                    for location_owner in location_owners:
                        location_ownerModel = LocationOwner(
                            current_owner=Country.objects.get(pk=location_owner['country_pk']),
                            room=cls.room,
                            location=Location.objects.get(pk=location_owner['location_pk']),
                        )
                        location_ownerModel.save()
                except (IOError, OSError,Exception) as e:
                    print("{} Error writing to file {}".format(type(e),e))
        except (FileNotFoundError, PermissionError, OSError):
            print("Error opening file")
            

    @classmethod
    def initializeTurnOrders(cls):
        for unit in Unit.objects.all():
            order = Order(instruction=MoveType.HOLD,
                        turn=cls.current_turn,
                        room=cls.room,
                        unit=unit,
                        current_location=unit.location)
            order.save()

    @classmethod
    def initialize(cls) -> None:
        cwd = os.getcwd()  
        # Initialise Database 
        cls.initializeDatabase(cwd)
        cls.initializeLocationOwners(cwd)
        cls.initializeUnits(cwd)

        # set first turn
        cls.room.current_turn = Turn.objects.get(year=1901, is_autumn=False, is_retreat_turn=False)
        cls.current_turn = cls.room.current_turn
        cls.initializeTurnOrders()
        cls.room.status = RoomStatus.WAITING
        if cls.room.map is None:
            cls.room.map = Map.objects.get(pk=1)
        cls.room.save()

    @classmethod
    def waiting(cls) -> None:  # wait for user to make a decision
        if cls.room.close_time is None:
            cls.room.set_close_time()
        elif cls.room.close_time <= datetime.datetime.now():
            # Check time, if past time go to resolve
            cls.room.status = RoomStatus.RESOLVE
            cls.room.save()

    @classmethod
    def resolve(cls) -> None:  # resolve orders
        LegitamiseOrders(cls.current_turn,cls.room)
        ResolveOrders(cls.current_turn,cls.room)
        # if some need to retreat
        retreaters = Outcome.objects.get_outcomes_retreat(cls.current_turn,cls.room)
        if len(retreaters) > 1:
            # increase to sub-turn
            if cls.current_turn.is_autumn:
                turn = Turn(year=cls.current_turn.year,
                            is_autumn=True, is_retreat_turn=True)
                turn.save()
            else:
                turn = Turn(year=cls.current_turn.year, is_retreat_turn=True)
                turn.save()
            cls.current_turn = turn
            # set all orders for this turn to hold
            cls.initializeTurnOrders()
            # send the retreaters to front end??

            cls.room.status = RoomStatus.RETREAT
            cls.room.save()
        else:
            cls.room.status = RoomStatus.UPDATE
            cls.room.save()

    @classmethod
    def retreat(cls) -> None:  # wait for user to make a decision on retreats
        if cls.room.close_time is None:
            cls.room.set_close_time()
        elif cls.room.close_time <= datetime.datetime.now():
            # check time, if past time go to resolve
            cls.room.status = RoomStatus.RESOLVE
            cls.room.save()

    @classmethod
    def update(cls) -> None:  # Update map with new Unit Positions
        # set temp retreat turn to different var
        retreat_turn = cls.current_turn
        # get turn from start of 'turn'
        cls.current_turn = Turn.objects.get(year=retreat_turn.year,
                                            is_autumn=retreat_turn.is_autumn,
                                            is_retreat_turn=False)
        # update unit positions
        Outcome.objects.perform_move_operations(retreat_turn,cls.room)
        Outcome.objects.perform_move_operations(cls.current_turn,cls.room)

        if cls.current_turn.is_autumn:
            cls.room.status = RoomStatus.RESUPPLY
            cls.room.save()
        else:
            cls.room.status = RoomStatus.CHECKING
            cls.room.save()

    @classmethod
    # TO-DO!
    def resupply(cls) -> None:  # Gaining Units After FALL

        # wait for user input on new unit location
        # or random?

        cls.room.status = RoomStatus.CHECKING
        cls.room.save()

    @classmethod
    def checking(cls) -> None:  # need to update the status to room app
        if cls.isFinished():
            cls.room.status = RoomStatus.CLOSED
            cls.room.save()
        else:
            # increase turn here!
            if cls.current_turn.is_autumn:
                turn = Turn(year=cls.current_turn.year+1)
                turn.save()
            else:
                turn = Turn(year=cls.current_turn.year, is_autumn=True)
                turn.save()
            cls.room.current_turn = cls.current_turn = turn
            cls.initializeTurnOrders()
            cls.room.status = RoomStatus.WAITING
            cls.room.save()
