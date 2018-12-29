import json
from user import User
from flask import Flask,jsonify

# json_user = jsonify({'user':user})

def printList(list):
    for l in list:
        print(l.__repr__())
    return

def dict_to_user(dict):
    new_user=User(dict['id'],dict['latitude'],dict['longitude'])
    return new_user

def dict_list_to_users(dict_list):
    user_list=[]
    for dict in dict_list:
        new_user = User(dict['id'], dict['latitude'], dict['longitude'])
        user_list.append(new_user)
    return user_list

#Transforms user_list into dict user list
def users_to_dict_list(list_users):
    dict_users=[]
    for user in list_users:
        dict_users.append(user.get_dict())
    return dict_users

# list_users = dict_list_to_users(users)
# print(list_users.__repr__())