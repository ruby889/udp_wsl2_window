import sys
import select
import signal
import socket
import sys
import time

class curi_communication_udp:
    name = 'udp'
    def __init__(self, receiveIP, receivePort, sendIP, sendPort):
        self.self_IP = receiveIP
        self.self_Port = receivePort
        self.target_Address = (sendIP, sendPort)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024)
        return
    
    def open(self):
        # self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.self_IP, self.self_Port))
        print('open socket')

    def close(self):
        print('close socket')
        self.s.close()

    def send(self, massage):
        self.s.sendto(massage.encode("utf-8"), self.target_Address)
        
    def receive(self, dt = 0.001): # waiting time
        readable = select.select([self.s], [], [], dt)[0]
        buf = ""
        if readable:
            for a in readable:
                buf = a.recvfrom(256)[0].decode("utf-8")
        return buf

    def set_start(self):
        self.send("start")

    def set_stop(self):
        self.send("stop")
        
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    CS.close()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    try:
        CS = curi_communication_udp("172.19.54.129", 10086, "172.19.48.1", 10085)
        CS.open()
        for i in range(10000):
            CS.send("1#2#3#4#5#")
            # data = CS.receive()
            # if data: print(data)
            time.sleep(0.05)
    except Exception as e: 
        print(e)
        print('exit')