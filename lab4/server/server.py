#!/usr/bin/env python

import Pyro4
import bookDB

# pyro4-nsc -n 193.136.128.108 -p 9090 list


Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')

def main():
        remoteLibrary = Pyro4.expose(bookDB.bookDB)

        db = bookDB.bookDB("mylib")


        daemon = Pyro4.Daemon(host = '192.168.65.129')

        ns = Pyro4.locateNS('193.136.128.109',9090)
        print (ns)

        try:
                ns.createGroup(':libraries')
        except:
                pass

        uri = daemon.register(db, "BookDB-78508_1")
        ns.register("BookDB-78508", uri)

        try:
                daemon.requestLoop()
        finally:
                daemon.shutdown(True)

if __name__=="__main__":
        main() 
