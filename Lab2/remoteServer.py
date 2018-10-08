import socket
# sudo lsof -i :12345
#

s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind(("0.0.0.0",port))
s.listen(5)
while True:
        c, addr = s.accept()
        print('Insert function name [Add, Push, Pop]')
        str=input()
        print('Connection from ', addr)
        c.send(str.encode())
        c.close()