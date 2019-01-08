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
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True
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

def get_connection():
    return pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name, autocommit=True)

def checkToken(token, username):
    if redis_client.get(username)==token:
        return True
    else:
        return False

def getDistance(lat1, lon1, lat2, lon2): 
    # approximate radius of earth in meters
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
    resp.set_cookie('username', username, secure=True)  #accessible in javascript
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
    cnx = get_connection()
    with cnx.cursor() as cursor:
        sql = "SELECT user_id FROM users;"
        cursor.execute(sql)
        result = cursor.fetchall()
    cnx.close()
    return jsonify(result)

@app.route('/sendMessage.html')
def sendMessage():
    if(not checkToken(session['access_token'], session['username'])):
        abort(403)
    else:
        return render_template('sendMessage.html')

@app.route('/nearbyUsers.html')
def check_nearby_users():
    if(not checkToken(session['access_token'], session['username'])):
        abort(403)
    else:
        return render_template('nearbyUsers.html')

@app.route('/index.html')
def indexHTML():
    if(not checkToken(session['access_token'], session['username'])):
        authorization_url='https://fenix.tecnico.ulisboa.pt/oauth/userdialog?client_id=1414440104755257&redirect_uri=https://asint-227116.appspot.com/callback'
        return redirect(authorization_url)
    else:
        return render_template('index.html')

#@app.route('/createBuilding', methods=['POST'])
#def createBuilding():
#    newname = request.json['newname']
#    newlatitude = request.json['newlatitude']
#    newlongitude = request.json['newlongitude']
#    newradius = request.json['newradius']
#    cnx = get_connection()
#    result = ""
#    with cnx.cursor() as cursor:
#        sql = "INSERT INTO buildings (building_name, latitude, longitude, radius) VALUES (%s, %s, %s, %s);"
#        cursor.execute(sql, (newname, newlatitude, newlongitude, newradius))
#        result = cursor.fetchall()
#    cnx.close()
#    return result


@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    if(checkToken(session['access_token'], session['username'])):
        resp.set_cookie('username', expires=0) 
        redis_client.delete(session['username'])
        session.pop('username')
    return resp


@app.route('/users', methods=['POST'])
def create_user():
    if(not checkToken(session['access_token'], session['username'])):
        abort(403)
    else:
        if not request.json or not 'id' in request.json or not 'latitude' in request.json or not 'longitude' in request.json:
            abort(400)
        user_info = ""
        cnx = get_connection()
        with cnx.cursor() as cursor:
            sql = "SELECT user_id, user_latitude, user_longitude FROM users;"
            cursor.execute(sql)
            result = cursor.fetchall()
            exists = False
            for users_now in result:
                if session['username'] == users_now[0]:
                    exists = True
                    user_info = users_now
                    break
            if exists == False:
                sql = "INSERT INTO users (user_id, user_latitude, user_longitude) VALUES (%s, %s, %s);"
                cursor.execute(sql, (session['username'], request.json['latitude'], request.json['longitude']))
            else:
                sql = "UPDATE users SET user_latitude = %s, user_longitude = %s WHERE user_id = %s;"
                cursor.execute(sql, (request.json['latitude'], request.json['longitude'], session['username']))
                if getDistance(float(user_info[1]), float(user_info[2]), float(request.json['latitude']), float(request.json['longitude']))>1:
                    #Create Move
                    with cnx.cursor() as cursor:
                        sql = "INSERT INTO user_move (user_id, old_latitude, old_longitude, new_latitude, new_longitude) VALUES (%s, %s, %s, %s, %s);"
                        cursor.execute(sql, (session['username'], user_info[1], user_info[2], request.json['latitude'], request.json['longitude']))
                        sql = "SELECT ID FROM user_move ORDER BY ID DESC LIMIT 1;"
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        sql = "INSERT INTO logs (content_id, user_id, entry_type) VALUES (%s, %s, 'Move');"
                        cursor.execute(sql, (result[0][0], session['username']))
        cnx.close()
        
        json_to_send = None
        return jsonify(json_to_send)

@app.route('/users/message', methods=['POST'])
def receive_user_message():
    if(not checkToken(session['access_token'], session['username'])):
        abort(403)
    else:
        if not request.json or not 'id' in request.json or not 'message' in request.json or not 'radius' in request.json:
            abort(400)
        
        json_to_send = None
        cnx = get_connection()
        with cnx.cursor() as cursor:
            sql = "INSERT INTO user_msg (user_id, msg_body, latitude, longitude, radius) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(sql, (session['username'], request.json['message'], request.json['latitude'], request.json['longitude'], request.json['radius']))
            sql = "SELECT ID FROM user_msg ORDER BY ID DESC LIMIT 1;"
            cursor.execute(sql)
            result = cursor.fetchall()
            sql = "INSERT INTO logs (content_id, user_id, entry_type) VALUES (%s, %s, 'Msg');"
            cursor.execute(sql, (result[0][0], session['username']))
        cnx.close()

        return jsonify(json_to_send)

@app.route('/users/messages_all', methods=['GET'])
def get_messages_all():
    if(not checkToken(session['access_token'], session['username'])):
        abort(403)
    else:
        this_user = None
        json_to_send = None
        
        cnx = get_connection()
        with cnx.cursor() as cursor:
            sql = "SELECT user_id, user_latitude, user_longitude FROM users;"
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                if row[0] == session['username']:
                    this_user = row
            if this_user != None:
                sql = "SELECT user_id, msg_body, latitude, longitude, radius from user_msg;"
                cursor.execute(sql)
                messages = cursor.fetchall()
                for message in messages:
                    data = {}
                    if getDistance(float(this_user[1]), float(this_user[2]), float(message[2]), float(message[3])) <= float(message[4]):              
                        data['id'] = str(message[0])
                        data['message'] = str(message[1])
                        json_data = json.dumps(data)
                        if(json_to_send == None):
                            json_to_send = json_data
                        else:
                            json_to_send = json_to_send + "," + json_data 
        cnx.close()
                            
        return jsonify(json_to_send)

@app.route('/nearbyUsers', methods=['POST'])
def get_nearby_users():
    if(not checkToken(session['access_token'], session['username'])):
        abort(403)
    else:
        radius = 10
        cnx = get_connection()
        with cnx.cursor() as cursor:
            sql = "SELECT user_id, user_latitude, user_longitude FROM users;"
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                if row[0] == session['username']:
                    this_user = row
            if this_user != None:      
                data = {}     
                for other_user in results:
                
                    if getDistance(float(this_user[1]), float(this_user[2]), float(other_user[1]), float(other_user[2])) <= radius:              
                        data['id'] = other_user[0]
                        json_data = json.dumps(data)
                        if(json_to_send == None):
                            json_to_send = json_data
                        else:
                            json_to_send = json_to_send + "," + json_data 
                            
        return jsonify(json_to_send)

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