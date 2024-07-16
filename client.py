import socket
from time import sleep
import select
def main(local_ip, local_port):
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server.bind((local_ip, local_port))
    print("Server Up And Listening")
    print("-----------------------")
    server.setblocking(0)

    while True:
        ready = select.select([server], [], [], 0.5)
        if ready[0]:
            bytes_adr_pair = server.recv(4096)
            msg = bytes_adr_pair[0]
            address = bytes_adr_pair[1]
            print("{} Sent: {}".format(address, msg))
        sleep(0.5)

if __name__ == "__main__":
    main("192.168.65.3", 6006)