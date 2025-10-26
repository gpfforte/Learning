import urllib.request
import json

req = urllib.request.Request("http://api.open-notify.org/iss-now.json")
response = urllib.request.urlopen(req)

obj = json.loads(response.read())
print(obj)
print(obj['timestamp'])
print(obj['iss_position'])