import csv
import pickle

with open('ISTCampee.data', 'rb') as filehandle:
    # read the data as binary data stream
    test_list = pickle.load(filehandle)

# for campee in test_list:
#     print(campee.__repr__())

list_buildings=[]

def countBuildings(campee_list):
    count = 0
    for campee in campee_list:
        for build in campee.list_of_buildings:
            build.name = build.name.decode('utf-8')
            list_buildings.append(build)
            count = count + 1
    return count

print("\nNumber of campee: "+ str(len(test_list)))
print("\nNumber of saved buildings: " + str(countBuildings(test_list)))


f = open('coordenadas.csv', encoding="utf-8")
reader = csv.DictReader( f, fieldnames=('espaco', 'latitude', 'longitude', 'radius'))

# for row in reader:
#     print(str(row))

for build in list_buildings:
    for row in reader:
        if build.name==row:
            build.latitude=200
    print(build.__repr__())


#Checks that value is passed by reference
for campee in test_list:
    print(campee.__repr__())