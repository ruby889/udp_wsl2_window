import sys
import time
import select
import signal
import socket
import traceback
from functools import partial

class curi_communication_udp:
    name = 'udp'
    def __init__(self, localIP, localPort, remoteIP, remotePort):
        self.self_IP = localIP
        self.self_Port = localPort
        self.target_Address = (remoteIP, remotePort)
        self.rx_buffer_size = 4096
        self.rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rx.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.rx_buffer_size)
        self.tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def open(self):
        # self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.rx.bind((self.self_IP, self.self_Port))
        self.tx.connect(self.target_Address)
        print('open socket')

    def close(self):
        self.tx.close()
        self.rx.close()
        print('close socket')

    def send(self, message):
        try:
            self.tx.send(message.encode("utf-8"))
        except ConnectionRefusedError:
            # print("Connection refused. Client may not be available.")
            return
        
    def receive(self, dt = 0.001): # waiting time
        readable = select.select([self.rx], [], [], dt)[0]
        buf = ""
        if readable:
            self.connected = True
            for a in readable:
                buf = a.recvfrom(self.rx_buffer_size)[0].decode("utf-8")
        return buf

def signal_handler(udp, sig, frame):
    print('You pressed Ctrl+C!')
    udp.close()
    sys.exit(0)
    
if __name__ == '__main__':
    CS = curi_communication_udp('localhost', 10086, 'localhost', 10085)
    signal.signal(signal.SIGINT,partial(signal_handler, CS))
    CS.open()
    for i in range(10000):
        CS.send("11#22#33#44#55#")
        data = CS.receive()
        if data: print(data)
        time.sleep(0.05)
