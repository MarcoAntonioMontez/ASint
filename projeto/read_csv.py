import csv
import pickle

with open('ISTCampee.data', 'rb') as filehandle:
    # read the data as binary data stream
    campeeList = pickle.load(filehandle)

list_buildings=[]

def countBuildings(campeeList ):
    count = 0
    for campee in campeeList :
        for build in campee.list_of_buildings:
            build.name = build.name.decode('utf-8')
            list_buildings.append(build)
            count = count + 1
    return count

print("\nNumber of campee: "+ str(len(campeeList )))
print("\nNumber of saved buildings: " + str(countBuildings(campeeList )))


f = open('coordenadas.csv', encoding="utf-8")
reader = csv.DictReader( f, fieldnames=('espaco', 'latitude', 'longitude', 'radius'))

for row in reader:
    for build in list_buildings:
        name=row['espaco']
        latitude = row['latitude']
        longitude = row['longitude']
        radius = row['radius']
        if name==build.name:
            build.latitude = latitude
            build.longitude = longitude
            build.radius = radius

# for campee in campeeList:
#     print(campee.__repr__())

# with open('ISTCampee.data', 'wb') as filehandle:
#     # store the data as binary data stream
#     pickle.dump(campeeList, filehandle)