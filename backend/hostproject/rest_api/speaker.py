import requests


def add_room(port, room_name:str):
    url = "http://127.0.0.1:"+str(port)+"/graphql/"
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
    query = query_template % room_name
    headers = { 'Content-Type': 'application/json' }
    data = {'query': query}
    res = requests.post(url, headers=headers, json=data).json()
    print(res)

    return res


def add_player(port:int, user_id:int, room_id:int):
    url = "http://127.0.0.1:"+str(port)+"/graphql/"
    query_template = '''
        mutation{
            createPlayer(userId: %s, roomId: %s){
                player{
                    id
                }
            }
        }
    '''
    query = query_template % (user_id, room_id)
    headers = { 'Content-Type': 'application/json' }
    data = {'query': query}
    res = requests.post(url, headers=headers, json=data).json()
    print(res)
    
    return res

def initialize(port:int, room_id:int):
    url = "http://127.0.0.1:"+str(port)+"/graphql/"
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
    query = query_template % room_id
    headers = { 'Content-Type': 'application/json' }
    data = {'query': query}
    res = requests.post(url, headers=headers, json=data).json()
    print(res)
    
    return res