from flask import Flask,jsonify,abort,make_response,request
import urllib3
import json
from campus import Campus
from builds import Building
from importCampee import ImportCampee
import pickle
from utils import *

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
        'latitude': 10.0000,
        'longitude': 10.0001
    },
    {
        'id': 'ist179021',
        'latitude': 10.0000,
        'longitude': 10.0002
    },
    {
        'id': 'ist178181',
        'latitude': 69,
        'longitude': 69
    }
]

campeeList = []

# {
#  "maps":[
#          {"id":"blabla","iscategorical":"0"},
#          {"id":"blabla","iscategorical":"0"}
#         ],
# "masks":
#          {"id":"valore"},
# "om_points":"value",
# "parameters":
#          {"id":"valore"}
# }
#
# data["maps"][0]["id"]  # will return 'blabla'
# data["masks"]["id"]    # will return 'valore'
# data["om_points"]





# {
#   "type" : "CAMPUS",
#   "id" : "2448131392438",
#   "name" : "Tecnologico e Nuclear",
#   "containedSpaces" : [ {
#     "type" : "ROOM",
#     "id" : "1691297991622663",
#     "name" : "Administracao",
#     "topLevelSpace" : {
#       "type" : "CAMPUS",
#       "id" : "2448131392438",
#       "name" : "Tecnologico e Nuclear"
#     }
#   },

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


@app.route('/asintproject/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})


@app.route('/asintproject/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})



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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


##Reads buildings from ist and stores them in campee_list

#campeeList=get_campee()
# for campee in campeeList:
#     print(campee.__repr__())

# with open('ISTCampee.data', 'wb') as filehandle:
#     # store the data as binary data stream
#     pickle.dump(campeeList, filehandle)

# with open('ISTCampee.data', 'rb') as filehandle:
#     # read the data as binary data stream
#     test_list = pickle.load(filehandle)


#printList(campeeList)
#print("\nNumber of saved buildings" + str(countBuildings(campeeList)) + "\nNum requested buildings" +
#      str(countBuildings(campeeList)))
print('\nCenas\n')

if __name__ == '__main__':
    app.run(debug=True)


#Get
#  curl -i http://localhost:5000/asintproject/users/ist178508


#POST
#curl -i -H "Content-Type: application/json" -X POST -d '{"id":"ist169699", "latitude":"30" , "longitude":"40"}' http://localhost:5000/asintproject/users
