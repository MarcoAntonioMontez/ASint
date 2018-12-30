from flask import Flask,jsonify,abort,make_response,request
import urllib3
import json
from campus import Campus
from builds import Building
import range
from importCampee import ImportCampee
import pickle
import utils
from message import Message

app = Flask(__name__)


##Isto podia ficar numa classe
buildingUrls = []
ur1="https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/2448131360898"
ur2="https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/2448131360897"
ur3="https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/2448131392438"

buildingUrls.append(ur1)
buildingUrls.append(ur2)
buildingUrls.append(ur3)


##Init de users para debug
users = [
    {
        'id': 'ist178508',
        'latitude': 38.811977, #Biblioteca
        'longitude': -9.094261
    },
    {
        'id': 'ist179021', #PavilhaodeCivil
        'latitude': 38.737466,
        'longitude': -9.140206
    },
    {
        'id': 'ist178181',
        'latitude': 38.737579, #TorreNorte
        'longitude': -9.138582
    },
{
        'id': 'ist176969',
        'latitude': 38.812030, #Biblioteca # 5meters from ist178508
        'longitude': -9.094262
    }
]

campeeList = []
message_list = []

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


@app.route('/asintproject/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})


@app.route('/asintproject/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})

@app.route('/asintproject/users/nearby/<string:user_id>/<string:radius>', methods=['GET'])
def get_user_nearby(user_id,radius):
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

@app.route('/asintproject/users/building/<string:building_name>', methods=['GET'])
def get_users_in_building(building_name):
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

@app.route('/asintproject/users', methods=['POST'])
def create_user():
    if not request.json or not 'id' in request.json or not 'latitude' in request.json or not 'longitude' in request.json:
        abort(400)
    user = {
        'id': request.json['id'],
        'latitude': request.json['latitude'],
        'longitude': request.json['longitude']
    }

    for existing_user in users:
        if user["id"] == existing_user["id"]:
            existing_user["latitude"] = user["latitude"]
            existing_user["longitude"] = user["longitude"]
            return jsonify({'existing_user': existing_user}), 201

    users.append(user)
    return jsonify({'user': user}), 201

@app.route('/asintproject/users/message', methods=['POST'])
def receive_user_message():
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

@app.route('/asintproject/users/messages_all', methods=['GET'])
def get_messages_all():
    messages_dict=[]
    for message in message_list:
        messages_dict.append(message.get_dict())
    return jsonify({'messages_all': messages_dict})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


#Get
#  curl -i http://localhost:5000/asintproject/users
#  curl -i http://localhost:5000/asintproject/users/ist178508

#  curl -i http://localhost:5000/asintproject/users/building/Biblioteca
#  curl -i http://localhost:5000/asintproject/users/building/PavilhaodeCivil
#  curl -i http://localhost:5000/asintproject/users/building/TorreNorte

#  curl -i http://localhost:5000/asintproject/users/nearby/ist178508/10




#POST
#curl -i -H "Content-Type: application/json" -X POST -d '{"id":"ist169699", "latitude":"30" , "longitude":"40"}' http://localhost:5000/asintproject/users

#curl -i -H "Content-Type: application/json" -X POST -d '{"id":"ist169699", "latitude":"38.811978" , "longitude":"-9.094261"}' http://localhost:5000/asintproject/users


#Enviar Menssagem
#curl -i -H "Content-Type: application/json" -X POST -d '{"id":"ist169699", "message":"Hello this is a message", "radius":"10", "latitude":"38.811978" , "longitude":"-9.094261"}' http://localhost:5000/asintproject/users/message

#Ver Log de mensagens
#curl -i http://localhost:5000/asintproject/users/messages_all