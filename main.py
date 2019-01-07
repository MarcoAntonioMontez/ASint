from flask import Flask, render_template, request, jsonify,abort,make_response, redirect, session, url_for
from math import sin, cos, sqrt, atan2, radians
from requests_oauthlib import OAuth2Session
import requests
import urllib3
import json
from campus import Campus
from builds import Building
from user import User
import range
from importCampee import ImportCampee
import pickle
import utils
from message import Message
from flask_cors import CORS
import fenixedu
import bmemcached
import os
import pymysql

config = fenixedu.FenixEduConfiguration.fromConfigFile('fenixedu.ini')
client = fenixedu.FenixEduClient(config)

base_url = 'https://fenix.tecnico.ulisboa.pt/'

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)
CORS(app)

redis_client = bmemcached.Client('memcached-18466.c3.eu-west-1-1.ec2.cloud.redislabs.com:18466', 'mc-KBY4m', 'otaT9lPXY9e3ppBnemshXeyIIvhBlAGL')

app.secret_key = 'SfPsJpv6wJTod6avb03fIjOKrzAMqH2H8gCyWklysIXU46CblYpcIdTZ6QNZLoAv1FX4JWgqGM2ed3Gp9jMoGw=='
client_id='1414440104755257'

##Isto podia ficar numa classe
buildingUrls = []
ur1="https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/2448131360898"
ur2="https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/2448131360897"
ur3="https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/2448131392438"

buildingUrls.append(ur1)
buildingUrls.append(ur2)
buildingUrls.append(ur3)

##Init de users para debug
users = []
move_list = []
campeeList = []
message_list = []

unix_socket = '/cloudsql/{}'.format(db_connection_name)

with open('ISTCampee_formated.data', 'rb') as filehandle:
    # read the data as binary data stream
    campee_list = pickle.load(filehandle)

##Print Campee list
# print("\nNumber of campee: "+ str(len(campee_list)))
#
# for campee in campee_list:
#     print(campee.__repr__())
#
# print("\nNumber of saved buildings" + str(countBuildings(campee_list)))

def countBuildings(campee_list):
    count = 0
    for campee in campee_list:
        for build in campee.list_of_buildings:
            count = count + 1
    return count

def get_campee() :
    print('\nget_campee\n')
    ICampee = ImportCampee(buildingUrls)
    campee_list = ICampee.get_campee();
    return campee_list

def get_building(campees,building_name):
    building=[]
    for campus in campees:
        for build in campus.list_of_buildings:
            formated_name=build.name
            if formated_name==building_name:
                building = build
                return building
    return building

def get_user_from_id(user_id):
    user = [user for user in users if user['id'] == user_id]
    return user[0]

def checkToken(token, username):
    if redis_client.get(username)==token:
        return True
    else:
        return False

def getDistance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373000.0
    lat1=radians(lat1)
    lon1=radians(lon1)
    lat2=radians(lat2)
    lon2=radians(lon2)  

    dlon = lon2 - lon1
    dlat = lat2 - lat1  

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    
    #distance between 1 and 2 in meters
    return distance

@app.route('/')
def login():
     return render_template('login.html')

@app.route('/redirect', methods=["POST"])
def my_redirect():
    authorization_url='https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=1414440104755257&redirect_uri=https://asint-227116.appspot.com/callback'
    return redirect(authorization_url)

@app.route('/callback', methods=["GET"])
def callback():
    config = fenixedu.FenixEduConfiguration.fromConfigFile('fenixedu.ini')
    client = fenixedu.FenixEduClient(config)
    base_url = 'https://fenix.tecnico.ulisboa.pt/'
    app.secret_key = 'SfPsJpv6wJTod6avb03fIjOKrzAMqH2H8gCyWklysIXU46CblYpcIdTZ6QNZLoAv1FX4JWgqGM2ed3Gp9jMoGw=='
    client_id='1414440104755257'
    
    tokencode = request.args.get('code')
    
    fenixuser = client.get_user_by_code(tokencode)
    person = client.get_person(fenixuser)
 
    username=person['username']
   
    token = fenixuser.access_token
    session['access_token']=token
    session['username']=username
    
    #escreve username-token na memcache REDIS, expirando depois de 10 minutos
    redis_client.set(username, token, 600)

    if(not checkToken(session['access_token'], session['username'])):
        authorization_url='https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=1414440104755257&redirect_uri=https://asint-227116.appspot.com/callback'
        return redirect(authorization_url)    

    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('username', username)
    return resp 

@app.route('/index', methods=["GET"])
def index():
    if(not checkToken(session['access_token'], session['username'])):
        authorization_url='https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=1414440104755257&redirect_uri=https://asint-227116.appspot.com/callback'
        return redirect(authorization_url)
    else:
        return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_users():
    if(not checkToken(session['access_token'], session['username'])):
        abort(403)
    else:
        return jsonify({'users': users})

@app.route('/sendMessage.html')
def sendMessage():
    if(not checkToken(session['access_token'], session['username'])):
        abort(403)
    else:
        return render_template('sendMessage.html')

@app.route('/index.html')
def indexHTML():
    if(not checkToken(session['access_token'], session['username'])):
        authorization_url='https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=1414440104755257&redirect_uri=https://asint-227116.appspot.com/callback'
        return redirect(authorization_url)
    else:
        return render_template('index.html')

@app.route('/logout')
def logout():
    if(checkToken(session['access_token'], session['username'])):
        redis_client.delete(session['username'])
        session.pop('username')
    return redirect(url_for('login'))


@app.route('/users', methods=['POST'])
def create_user():
    if(not checkToken(session['access_token'], session['username'])):
        abort(403)
    else:
        if not request.json or not 'id' in request.json or not 'latitude' in request.json or not 'longitude' in request.json:
            abort(400)
        user = {
            'id': request.json['id'],
            'latitude': request.json['latitude'],
            'longitude': request.json['longitude']
        }

        for existing_user in users:
            if user["id"] == existing_user["id"]:
                if existing_user["latitude"] != user["latitude"] or existing_user["longitude"] != user["longitude"]:
                    #Create Move
                    move = {
                        'id': user["id"],
                        'old_latitude': existing_user["latitude"],
                        'old_longitude': existing_user["longitude"],
                        'new_latitude': user["latitude"],
                        'new_longitude': user["longitude"],
                    }
                    move_list.append(move)
                    existing_user["latitude"] = user["latitude"]
                    existing_user["longitude"] = user["longitude"]
                return jsonify({'existing_user': existing_user}), 201

        users.append(user)
        return jsonify({'user': user}), 201

@app.route('/users/message', methods=['POST'])
def receive_user_message():
    if(not checkToken(session['access_token'], session['username'])):
        abort(403)
    else:
        if not request.json or not 'id' in request.json or not 'message' in request.json or not 'radius' in request.json:
            abort(400)
        message_dict = {
            'id': request.json['id'],
            'message': request.json['message'],
            'radius': request.json['radius'],
            'latitude': request.json['latitude'],
            'longitude': request.json['longitude']
        }

        message = Message(message_dict)
        message_list.append(message)

        return jsonify({'message': message_dict}), 201

@app.route('/users/messages_all', methods=['GET'])
def get_messages_all():
    if(not checkToken(session['access_token'], session['username'])):
        abort(403)
    else:
        json_to_send = None
        this_user = [user for user in users if user['id'] == session['username']]
        print(this_user)
        for message in message_list:
            data = {}
            msg = message.get_dict()
            
            if getDistance(this_user['latitude'], this_user['longitude'], msg['latitude'], msg['longitude']) <= msg['radius']:                
                data['id'] = str(msg['id'])
                data['message'] = str(msg['message'])
                json_data = json.dumps(data)
                if(json_to_send == None):
                    json_to_send = json_data
                else:
                    json_to_send = json_to_send + "," + json_data 
                         
        return jsonify(json_to_send)

@app.route('/testestest2', methods=['GET'])
def testar2():
 current_time = ""
 if(not checkToken(session['access_token'], session['username'])):
    abort(403)
 else:
  cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
  with cnx.cursor() as cursor:
   cursor.execute('SELECT * FROM users;')
   result = cursor.fetchall()
   current_time = result[0][0]
  cnx.close()

 return str(current_time)

#----------------------------------------------------------------------------------------------------#
@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    if(not checkToken(session['access_token'], session['username'])):
        abort(403)
    else:
        user = [user for user in users if user['id'] == user_id]
        if len(user) == 0:
            abort(404)
        return jsonify({'user': user[0]})

@app.route('/users/nearby/<string:user_id>/<string:radius>', methods=['GET'])
def get_user_nearby(user_id,radius):
    if(not checkToken(session['access_token'], session['username'])):
        abort(403)
    else:
        radius = float(radius)
        #transform dict list to user list
        user_list=utils.dict_list_to_users(users)
        #get corresponding dict_user
        client_user_dict=get_user_from_id(user_id)
        # transform dict_user to user
        client_user=utils.dict_to_user(client_user_dict)

        #Get users nearby
        nearby_users=range.nearby_users(user_list,client_user,radius)
        # Store users as dict_users
        nearby_users_dict=utils.users_to_dict_list(nearby_users)
        if len(nearby_users_dict) == 0:
            abort(404)
        return jsonify({'nearby_users': nearby_users_dict})

@app.route('/users/building/<string:building_name>', methods=['GET'])
def get_users_in_building(building_name):
    if(not checkToken(session['access_token'], session['username'])):
        abort(403)
    else:
        #Falta tirar os acentos dos edificios
        building = get_building(campee_list,building_name)
        if building == []:
            abort(404)

        lat=float(building.latitude)
        long=float(building.longitude)
        rad=float(building.radius)
        # return jsonify({'name': building.name})
        user_list=[]
        for user in users:
            u_lat=user["latitude"]
            u_long=user["longitude"]
            if range.is_in_range(u_lat,u_long,lat,long,rad):
                user_list.append(user)
        return jsonify({'users': user_list})
#--------------------------------------------------------------------------------------------------#
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(403)
def forbidden(error):
    return make_response(jsonify({'error': 'Forbidden'}), 403)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8080)