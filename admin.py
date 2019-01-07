import getpass
import requests


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
        
    elif (command=='list_all_users'):
        url = new URL("https://asint-227116.appspot.com/users?admin=69);
        r = requests.get(url)
        print(r.content)
    #elif (command=='list_users_building'):

    #elif (command=='list_logs'):