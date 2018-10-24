#Entrar no DNS
#ver todos os srvidores e guardar as bases de dados

import Pyro4
import dbUI

class proxy_DB:

    def __init__(self,ip,port,ns):
        self.ip=ip
        self.port=port
        self.ns=ns

    def list_all(self):
        ns = Pyro4.locateNS(self.ip, self.port)
        servers=ns.list('BookDB')
        for server in servers:
            print(server)

    def get_all_servers(self):
        list_servers = []
        ns = Pyro4.locateNS(self.ip, self.port)
        servers = ns.list('BookDB')
        return servers
    #Receber all dbs

    def join_db(self):
        print('Mile1')
        list_uri=[]
        servers=self.get_all_servers()
        for uri in servers.values():
            list_uri.append(Pyro4.Proxy(uri))
            print(uri)

        db=list_uri[5]
        ui = dbUI.dbUI(db)
        ui.menu()

        # list_rows=[]
        # for db in list_db:
        #     rows=db.list_all_books()
        #     for row in rows:
        #         print(row)
        # return(list_rows)
