import json
from graphene_django.utils.testing import GraphQLTestCase

class MyFancyTestCase(GraphQLTestCase):
    def test_some_query(self):
        response = self.query(
            '''
            query{
                orders{
                    id
                    targetUnit{
                        id
                    }
                }
            }
            ''',
            op_name='myModel'
        )

        content = json.loads(response.content)

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)

        # Add some more asserts if you like
        ...