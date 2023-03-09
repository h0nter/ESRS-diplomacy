from graphene_django.utils.testing import GraphQLTestCase
import json
from room.tests.initial_insert import InitialInsert as II

class MyFancyTestCase(GraphQLTestCase):
    def test_some_query(self):
        II.all_insert()
        for tableName in ['turns', 'units', 'orders', 'locations']:
            querySyntax = "query{ " + tableName + " {id} }"
            response = self.query(querySyntax)
            content = json.loads(response.content)
            print(content)

            # This validates the status code and if you get errors
            self.assertResponseNoErrors(response)
        