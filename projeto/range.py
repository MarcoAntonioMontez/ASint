import utils

def distance(latitude1, longitude1, latitude2, longitude2):
    from math import sin, cos, sqrt, atan2, radians

    lat1 = radians(float(latitude1))
    lon1 = radians(float(longitude1))
    lat2 = radians(float(latitude2))
    lon2 = radians(float(longitude2))

    # approximate radius of earth in km
    r = 6373.0

    dlon = lon1 - lon2
    dlat = lat1 - lat2

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return r * c * 1000


def is_in_range(a1, a2, b1, b2, radius):
    if distance(a1, a2, b1, b2) <= float(radius):
        return 1
    else:
        return 0

#Receives user objets
def is_user_in_range(user1,user2,radius):
    [lat1,long1]=user1.get_position()
    [lat2, long2] = user2.get_position()
    return is_in_range(lat1,long1,lat2,long2,radius)

#Receives user objets
def nearby_users(list_users,ask_user,radius):
    nearby_users=[]
    for user in list_users:
        if is_user_in_range(user,ask_user,radius):
            nearby_users.append(user)
    return nearby_users




# dict_users = [
#     {
#         'id': 'ist178508',
#         'latitude': 38.811977, #Biblioteca
#         'longitude': -9.094261
#     },
#     {
#         'id': 'ist179021', #PavilhaodeCivil
#         'latitude': 38.737466,
#         'longitude': -9.140206
#     },
#     {
#         'id': 'ist178181',
#         'latitude': 38.737579, #TorreNorte
#         'longitude': -9.138582
#     },
# {
#         'id': 'ist176969',
#         'latitude': 38.812030, #Biblioteca # 5meters from ist178508
#         'longitude': -9.094262
#     }
# ]
#
# users = utils.dict_list_to_users(dict_users)
# # print(users.__repr__())
#
# nearby_users = nearby_users(users,users[0],10)
# print(nearby_users.__repr__())
#
# dict_list=utils.users_to_dict_list(nearby_users)
# print(dict_list)

# lat_a=38.736766
# long_a= -9.139065
#
# lat_b=38.737188
# long_b=-9.139133
#
# dist=distance(lat_a,long_a,lat_b,long_b)
# print("distance is: "+ str(dist))
#answer should be 47 meters

# lat_a=38.811977
# long_a= -9.094261
#
# lat_b=38.812030
# long_b=-9.094262
#
# dist=distance(lat_a,long_a,lat_b,long_b)
# print("distance is: "+ str(dist))
# #distance=5.8meters
