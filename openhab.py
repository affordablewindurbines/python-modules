import requests

command = "Turn oFF Bedroom FAN"
string = "http://localhost:8080/CMD?VoiceCommand=" + str(command)
r = requests.get(string, auth=('user', 'password')) 
print r.status_code
