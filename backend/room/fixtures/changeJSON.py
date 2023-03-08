#Not needed but nice to keep a copy for future changes

import commentjson
import copy

with open('./location.json','r') as j:
    location = commentjson.loads(j.read())

with open('./next_to.json','r') as j:
    next_to = commentjson.loads(j.read())

newdata = []
x = 0
start = {"model":"room.next_to","pk":x,"fields":{}}
#print(data)
for k in next_to:
    cur_loc = list(filter(lambda x:x["fields"]["name"]==k,location))[0]["pk"]
    print('cur ' + k)

    start["fields"]["location"] = cur_loc
    #print(polygons[k])
    for p in next_to[k]:
        print('next ' +p)
        temp_loc = list(filter(lambda x:x["fields"]["name"]==p,location))[0]["pk"]
        #print(temp_loc)
        start["pk"] = x
        start["fields"]["next_to"] = temp_loc
        x += 1
        print(start)
        newdata.append(copy.deepcopy(start))
        #print(newdata)

print(newdata)
with open('data.json', 'w', encoding='utf-8') as f:
    commentjson.dump(newdata, f, ensure_ascii=False, indent=4)
