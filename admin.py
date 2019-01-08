import getpass
import requests
import urllib
import json

print('Please Login \n')
username = input("Username: ")  # Python 3
password = getpass.getpass('Password: ')

if(username=='admin' and password=='123'):
	print("\nWelcome admin.\n")
    
print('type "help" to see available commands')
while(1):
    
    command = input('admin@asint: ')

    if(command=='help'):
        print('commands available:\n "add_building" ->add new building \n "list_all_users" -> list all connected users \n "list_users_building" -> list all users inside a certain building \n "list_logs" -> list all users movements and exchanged messages')    
    #elif (command=='add_building'):
    #    newname = input('new building name: ')
    #    newlatitude = input('new building latitude: ')
    #    newlongitude = input('new building longitude: ')
    #    newradius = input('new building radius: ')
    #
    #   builddata = {"newname": newname, "newlatitude": newlatitude, "newlongitude": newlongitude, "newradius": newradius}
    #
    #    url = "https://asint-227116.appspot.com/createBuilding"
    #    r = requests.post(url, data=json.dumps(builddata))   
    #    
    elif (command=='list_all_users'):
        url = "https://asint-227116.appspot.com/users"
        r = requests.get(url)
        print(r.content)
    #elif (command=='list_users_building'):

    #elif (command=='list_logs'):