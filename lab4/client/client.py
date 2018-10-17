#!/usr/bin/env python

import Pyro4
import dbUI


Pyro4.config.SERIALIZER = 'pickle'

def main():
        ns = Pyro4.locateNS('193.136.128.108',9090)
        uri = ns.lookup('BookDB')
        
        db = Pyro4.Proxy(uri)

        
        ui = dbUI.dbUI(db)
        ui.menu()

if __name__=="__main__":
        main() 
