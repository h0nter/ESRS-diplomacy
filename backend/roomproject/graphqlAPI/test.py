from graphene_django.utils.testing import GraphQLTestCase
import requests

from room.models.room import Room
from room.models.location import Location, Next_to
from room.models.map import Map
from room.models.country import Country
from room.models.order import Order
from room.models.turn import Turn
from room.models.unit import Unit

class MyFancyTestCase(GraphQLTestCase):

     # setup test database to use throughout this class
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.map = Map.objects.create(name="A test map", max_countries=7)
        cls.turn = Turn.objects.create(year=1994)
        cls.room = Room.objects.create(current_turn=cls.turn,room_name='test Room')
        cls.countryA = Country.objects.create(name="country A", map=cls.map,colour='red')
        cls.locationA = Location.objects.create(name="location A",map=cls.map)
        cls.locationB = Location.objects.create(name="location B",map=cls.map)
        cls.nextToAB = Next_to.objects.create(location=cls.locationA, next_to=cls.locationB)
        cls.nextToBA = Next_to.objects.create(location=cls.locationB, next_to=cls.locationA)
        cls.unitA = Unit.objects.create(owner=cls.countryA,location=cls.locationA,room=cls.room)
        cls.orderA = Order.objects.create(instruction='MVE', turn=cls.turn, room=cls.room, unit=cls.unitA, current_location=cls.locationA, target_location=cls.locationB)


    def test_some_query(self):
        # for tableName in ['turn', 'unit', 'order', 'location']:
        #     querySyntax = "query{ " + tableName + " {id} }"
        #     response = self.query(querySyntax)
        #     content = json.loads(response.content)
        #     #print(content)

        #     # This validates the status code and if you get errors
        #     self.assertResponseNoErrors(response)

        url = "http://127.0.0.1:"+str(8000)+"/graphql/"
        query_template = '''
            mutation{
                initilizeRoom(roomId: %s){
                    room{
                        id,
                        status
                    }
                }
            }
        '''
        query = query_template % 1
        headers = { 'Content-Type': 'application/json' }
        data = {'query': query}
        res = requests.post(url, headers=headers, json=data).json()
        