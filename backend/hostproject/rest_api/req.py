import requests

url = "http://127.0.0.1:8080/graphql"

query_template = '''
mutation{
  createRoom(roomName:" %s "){
    room{
      id,
      roomName
    }
  }
}
'''
query = query_template % 12

headers = { 'Content-Type': 'application/json' }

data = {'query': query}

response = requests.post(url, headers=headers, json=data)
response_data = response.json()
# Print the response data
print(response_data['data']['createRoom']['room']['id'])