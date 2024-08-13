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
        return
    
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
        self.tx.send(message.encode("utf-8"))
        
    def receive(self, dt = 0.001): # waiting time
        readable = select.select([self.rx], [], [], dt)[0]
        buf = ""
        try:
            if readable:
                for a in readable:
                    buf = a.recvfrom(self.rx_buffer_size)[0].decode("utf-8")
        except e:
            # if isinstance(e, WindowsError) and e.winerror == 10040:
            traceback.print_exc()
        return buf

    def set_start(self):
        self.send("start")

    def set_stop(self):
        self.send("stop")
        
def signal_handler(udp, sig, frame):
    print('You pressed Ctrl+C!')
    udp.close()
    sys.exit(0)
    
if __name__ == '__main__':
    try:
        CS = curi_communication_udp("10.30.7.78", 10085, "10.30.7.152", 10086)
        signal.signal(signal.SIGINT,partial(signal_handler, CS))
        CS.open()
        for i in range(10000):
            CS.send("1#2#3#4#5#")
            data = CS.receive()
            if data: print(data)
            time.sleep(0.05)
    except Exception as e: 
        print(e)
        print('exit')
