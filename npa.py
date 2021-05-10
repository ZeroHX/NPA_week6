import requests
import json
from datetime import datetime, timedelta

# Access token change every 12 hrs
access_token = 'YzRjM2YxNDItMWZiNy00OWJkLWIyOTEtNjczZTdlNmRmZGQ1OWM4ODZlNmYtYWRk_P0A1_408b8cf5-9f52-48d9-be13-2cd9891ab13f'

url = 'https://webexapis.com/v1/messages'
url_room = 'https://webexapis.com/v1/rooms'
url_geo = "http://www.mapquestapi.com/geocoding/v1/address"
room_id = 'Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vZjc5YjRkNzAtNWExNy0xMWViLThiMGEtNWZkOTY0MzU0ZDUx'
headers = {
 'Authorization': 'Bearer {}'.format(access_token),
 'Content-Type': 'application/json'
}
params={'max': '100'}
res = requests.get(url_room, headers=headers, params=params)
print("List of room:")
lst_room = []
num = 1
for i in res.json()['items']:
    print("- [%d] %s"%(num, i['title']))
    lst_room.append({'id':i['id'],'title':i['title']})
    num += 1

room = lst_room[int(input("Which room does you want to mornitored? (Type number): "))-1]
room_id = room["id"]

def get_iss(lat,lng, country):
    res_iss = requests.get('http://api.open-notify.org/iss-pass.json?lat=%s&lon=%s'%(lat,lng))
    time_lst = res_iss.json()['response'][0]
    dt = (datetime.fromtimestamp(time_lst['risetime']) + timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S')
    txt = '> In %s the ISS will fly over on %s for %s seconds.'%(country,dt, time_lst['duration'])
    createMsg(txt)
def createMsg(msg):
    params_createMsg = {
    'roomId': room_id,
    "text": msg
    }
    requests.post(url, headers=headers, json=params_createMsg)

def createFile(f):
    params_createFile = {
    'roomId': room_id,
    "file": f
    }
    requests.post(url, headers=headers, json=params_createFile)

def getMsg():
    params = {
        'roomId': room_id
    }
    res = requests.get(url, headers=headers, params=params)
    # print(json.dumps(res.json(), indent=1))
    current_msg = res.json()['items'][0]['text']
    return current_msg
#for test
# createMsg("/Bangkok")
# createFile("https://media2.giphy.com/media/9PnLL17VuvQ9ixhCZw/giphy.gif?cid=8d48595f8cf04b9e4e3a8e88450dc9f33b688fdce24dfdfa&rid=giphy.gif&ct=g")
while True:
    try:
        headers = {
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
        }
        
        current_msg = getMsg()
        print("Current Message: %s"%current_msg)



        if "/lovecalc"in current_msg:
            url_love = "https://love-calculator.p.rapidapi.com/getPercentage"
            msg = "> Love Calculator <3 :"
            createMsg(msg)
            love, fname,sname = current_msg.split()
            querystring = {"fname":fname,"sname":sname}
            headers_love = {
                'x-rapidapi-key': "03213dc232msh70eefe81ba70b92p18bf77jsn73c177101805",
                'x-rapidapi-host': "love-calculator.p.rapidapi.com"
                }
            response_love = requests.request("GET", url_love, headers=headers_love, params=querystring)
            createMsg("> Name: %s %s"%(fname,sname))
            createMsg("> Matching . . . [%s %%]"%(response_love.json()["percentage"]))
            createMsg("> Result: %s"%(response_love.json()["result"]))

        elif "/randomGif" in current_msg:
            tag = current_msg.split()[1]
            url_rand = "https://api.giphy.com/v1/gifs/random?api_key=YfooEqiPoIBMNmDuye7Y6ge7uKRzPX8q&tag=%s&rating=pg"%tag
            response = requests.request("GET", url_rand)
            createFile(response.json()['data']['images']['downsized']['url'])

        elif current_msg[0] == "/":
            action = current_msg[1:]
            print(action)
            params_geo = {
            'key': '',  #key geo
            'location': action
            }
            
            res_geo = requests.get(url_geo, params=params_geo)
            lat_lng = res_geo.json()['results'][0]['locations'][0]['latLng']
            txt = "> Latitude: %f\tLongitude: %f"%(lat_lng['lat'],lat_lng['lng'])
            createMsg(txt)
            get_iss(lat_lng['lat'],lat_lng['lng'], action)

    except KeyboardInterrupt:
        print("\n\nExit . . .")
        break
    except:
        print("Not a message format.")
