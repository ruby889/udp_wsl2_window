import socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    client_ip = "127.0.0.1"
    client_port = 6116
    s.connect((client_ip, client_port))
    print(s.send(b"Hello World"))