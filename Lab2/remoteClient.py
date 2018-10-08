import socket

s = socket.socket()

# host = socket.gethostname()
host = '194.210.229.202'
port = 8001
s.connect((host, port))
print(s.recv(1024).decode())
# print('Falei com o servidor!!')
s.close
