import sys
from curi_udp import curi_communication_udp
import numpy as np
import time
import sys
import signal
class cuarm_udp:
    def __init__(self, receiveIP, receivePort, sendIP, sendPort):
        self.udp = curi_communication_udp(receiveIP, receivePort, sendIP, sendPort)
        self.udp.open()
    
    def receive(self):
        raw = self.udp.receive()
        splited = raw[2:].split('#')[:-1]
        data = {}
        if len(splited) >= 4:
            data['RunningState']    = int(splited[0])
            data['JointSize']       = int(splited[1])
            data['CommandMode']     = int(splited[2])
            data['Target']    = np.array([float(ele) for ele in splited[3].split('$')[:-1]])
        return data
    
    def send(self, message):
        self.udp.send(message)
        
    def __del__(self):
        self.udp.close()
        
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    CS.close()
    sys.exit(0)
    
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    try:
        CS = cuarm_udp("172.19.48.1", 10085, "172.19.54.129", 10086)
        while True:
            # CS.send("9#2#3#4#5#")
            data = CS.receive()
            if data: print(data)
            time.sleep(0.05)
    except Exception as e: 
        print(e)
        print('exit')