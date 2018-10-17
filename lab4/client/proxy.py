#Entrar no DNS
#ver todos os srvidores e guardar as bases de dados

import Pyro4
import dbUI

class proxy_DB:

    def __init__(self,ip,port):
        self.ip=ip
        self.port=port

    def list_all(self):
        ns = Pyro4.locateNS(self.ip, self.port)
        servers=ns.list('BookDB')
        for server in servers:
            print(server)

        #Receber all dbs