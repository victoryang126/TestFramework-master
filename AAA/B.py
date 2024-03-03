import socket

server_address = ('0.0.0.0', 8888)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)

print('服务器正在等待连接...')

# 接受连接
client_socket, client_address = server_socket.accept()
print(f'已连接客户端：{client_address}')

# 接收数据
data = client_socket.recv(1024)
print(f'接收到的数据：{data.decode("utf-8")}')

# 关闭与客户端的连接
client_socket.close()
server_socket.close()
