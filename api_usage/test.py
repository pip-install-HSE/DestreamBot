import urllib.parse
import urllib.request
import requests

getUserUrl = "https://exp.destream.net/api/v1/telegram-bot/user"
secondUrl = "https://exp.destream.net/api/v1/telegram-bot/donation"

# url = "https://exp.destream.net/api/v1/telegram-bot/user"
# header={"x-api-key" : 'user1-secret-access-token'}
# # post_param = urllib.parse.urlencode({
# #                 'user' : 'tweetbotuser',
# #        'status-update' : 'alientest'
# #       }).encode('UTF-8')
# post_param = urllib.parse.urlencode({})
#
# req = urllib.request.Request(url, post_param, header)
# response = urllib.request.urlopen(req)
#
# print(response.read())

params = {"X-API-KEY": "user1-secret-access-token"}
r = requests.get(getUserUrl, headers=params)
print(r.status_code)
# if r.status_code == 200
print(r.json())

params = {
"currency":"RUB",
"amount":1100,
"message":"ololo",
"additionalParameters":{
 "usr_id":"123456-loo",
 "group_id":44784
 }
}

headers={'Content-type':'application/json', 'Accept':'application/json', "X-API-KEY": "user1-secret-access-token"}
r = requests.post(secondUrl, json=params, headers=headers)
print(r.json())