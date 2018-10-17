#!/usr/bin/env python

import Pyro4
import dbUI
import proxy

Pyro4.config.SERIALIZER = 'pickle'

def main():
        ns = Pyro4.locateNS('193.136.128.108',9090)
        uri = ns.lookup('BookDB-78508')
        
        db = Pyro4.Proxy(uri)

        proxy_server=proxy.proxy_DB('193.136.128.108',9090)
        proxy_server.list_all()

        #ui vai receber uma lista de base de dados
        #usando um proxy
        ui = dbUI.dbUI(db)
        ui.menu()

if __name__=="__main__":
        main() 
