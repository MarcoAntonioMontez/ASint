import socket
import pickle

s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind((host,port))
s.listen(5)
while True:
    c, addr = s.accept()
    print('Connection from ', addr)
    # c.send('Hello'.encode())
    data = c.recv(4096)
    data_arr=pickle.loads(data)
    print(data_arr)
    garbage=c.recv(1024)

    c.close()
        #comment