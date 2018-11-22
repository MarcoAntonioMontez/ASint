users = [
    {
        'id': 'ist178508',
        'latitude': "10.0000",
        'longitude': 10.0001
    },
    {
        'id': 'ist179021',
        'latitude': "10.0000",
        'longitude': 10.0002
    }
]

user = {
        'id': 'ist178508',
        'latitude': "10.0000",
        'longitude': 20.00
    }


for existing_user in users:
    if user["id"]==existing_user["id"]:
        existing_user["latitude"]=user["latitude"]
        existing_user["longitude"]=user["longitude"]
        break
print(users)