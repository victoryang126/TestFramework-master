import socket

# 服务器的地址和端口号
server_address = ('127.0.0.1', 9999)

# 创建数据报套接字
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(server_address)

print('服务器正在等待数据...')

# 接收数据
data, client_address = udp_socket.recvfrom(1024)
print(f'接收到的数据：{data.decode("utf-8")}, 来自客户端：{client_address}')

# 关闭套接字
udp_socket.close()
