#Not needed but nice to keep a copy for future changes

import json
import copy


with open('./unit.json','r') as j:
    location = json.loads(j.read())

# with open('./unit.json','r') as j:
#     order = commentjson.loads(j.read())

newdata = {1:[]}
x = 0
#start = {"model":"room.next_to","pk":x,"fields":{}}
#print(data)
# for k in location:
#     print(k)
#     cur_loc = list(filter(lambda x:x["name"]==k['fields']['name'],territories))[0]['text']
#     print(cur_loc)
#     k["fields"]["abbreviation"] = copy.deepcopy(cur_loc)

for k in location:
    #
    # cur_loc = list(filter(lambda x:x["fields"]["'name'"]==k,location))[0]["pk"]
    #print(k)
    # if k["fields"]['map'] not in newdata:
    #     newdata[k["fields"]['map']] = []

    # if 'current_owner' in k['fields']:
    #     print(k["fields"]["name"],k["fields"]["current_owner"])
    newdata[1].append({'unit_owner': k["fields"]['owner'],'unit_location': k["fields"]["location"],'unit_can_float': k["fields"]["can_float"]})

    # start["fields"]["location"] = cur_loc
    # #print(polygons[k])
    # for p in next_to[k]:
    #     print('next ' +p)
    #     temp_loc = list(filter(lambda x:x["fields"]["'name'"]==p,location))[0]["pk"]
    #     #print(temp_loc)
    #     start["pk"] = x
    #     start["fields"]["next_to"] = temp_loc
    #     x += 1
    #     print(start)
    #     newdata.append(copy.deepcopy(start))
    #     #print(newdata)

print(newdata)
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(newdata, f, ensure_ascii=False, indent=4)
