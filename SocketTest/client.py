import socket

# 服务器的地址和端口号
server_address = ('127.0.0.1', 9999)

# 创建数据报套接字
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 发送数据到服务器
message = 'Hello, server!'
udp_socket.sendto(message.encode('utf-8'), server_address)

# 关闭套接字
udp_socket.close()
