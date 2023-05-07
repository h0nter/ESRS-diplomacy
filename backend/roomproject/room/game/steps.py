from room.game.legitamiseOrders import LegitamiseOrders
from room.game.resolveOrders import ResolveOrders
from room.models.room import RoomStatus
from room.models.order import Order, MoveType
from room.models.outcome import Outcome
from room.models.turn import Turn
from room.models.unitTypes import Unit
from django.core.management import call_command

class Step:

    @classmethod
    def room_factory(cls, room_id):
        return cls(room_id)

    @classmethod
    def isFinished(cls) -> bool:
        return True

    @classmethod
    def initializeTurnOrders(cls):
        for unit in Unit.objects.all():
            order = Order(instruction=MoveType.HOLD,
                          turn=cls.current_turn,
                          target_unit=unit,
                          current_location=unit.location)
            order.save()

    @classmethod
    def initialize(cls) -> None:  # format the room database
        call_command('loaddata', 'room/fixtures/*json')

        # set first turn
        cls.room.current_turn = Turn.objects.get(year=1901, is_autumn=False)
        cls.current_turn = cls.room.current_turn

        cls.room.status = RoomStatus.OPEN
        cls.room.save()

    @classmethod
    # wait for user to login the game, then call this.
    def opening(cls) -> None:

        cls.initializeTurnOrders()

        # does anything need to go in here?

        cls.room.status = RoomStatus.WAITING
        cls.room.save()

    @classmethod
    def waiting(cls) -> None:  # wait for user to make a decision

        # Check time, if past time go to resolve
        cls.room.status = RoomStatus.RESOLVE
        cls.room.save()

    @classmethod
    def resolve(cls) -> None:  # resolve orders
        LegitamiseOrders(cls.current_turn)
        ResolveOrders(cls.current_turn)
        # if some need to retreat
        retreaters = Outcome.objects.get_outcomes_retreat(cls.current_turn)
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
        Outcome.objects.perform_move_operations(retreat_turn)
        Outcome.objects.perform_move_operations(cls.current_turn)

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
