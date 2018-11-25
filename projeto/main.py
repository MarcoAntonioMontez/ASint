#import user, builds, campus
from user import User
from campus import Campus
from builds import Building
from range import is_in_range


def main():
    user1 = User(178779, 10, 20)
    user2 = User(178181, 40, 40)

    alameda = Campus(1, 'Alameda')

    torreNorte = Building(1, 'Torre Norte', alameda.id, 10, 20, 20)

    print(is_in_range(torreNorte.latitude, torreNorte.longitude, user1.latitude, user1.longitude, torreNorte.radius))
    print(is_in_range(torreNorte.latitude, torreNorte.longitude, user2.latitude, user2.longitude, torreNorte.radius))


if __name__ == '__main__':
    main.run(debug=True)