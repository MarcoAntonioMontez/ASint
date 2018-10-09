import socket
import pickle

s = socket.socket()

host = socket.gethostname()
port = 12345
s.connect((host,port))
# print(s.recv(1024))
# print('Falei com o servidor!!')

array = ["artur","marco"]
print(array)
byte_array=pickle.dumps(array)
s.send(byte_array)

s.close