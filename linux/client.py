import socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect(("172.19.48.1", 6006))
    print(s.send(b"Hello World"))