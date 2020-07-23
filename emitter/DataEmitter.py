import socket
import json


class DataEmitter:

    def __init__(self, MCAST_GROUP='224.0.0.1', MCAST_PORT=12000, debug=False):
        self.MCAST_GRP = MCAST_GROUP
        self.MCAST_PORT = MCAST_PORT
        self.debug = debug
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.sent = 0

    def emit(self, data: dict):
        try:
            js = json.dumps(data)
            self.sock.sendto(js.encode(), (self.MCAST_GRP, self.MCAST_PORT))
            self.sent += 1
            if self.debug:
                print('[EMIT]', js)
                print('[SIZE]', len(js.encode()))
        except Exception as e:
            raise e
            if self.debug:
                print('[EMIT ERROR]')
            self.close()

    def reset(self):
        self.sent = 0

    def close(self):
        self.sock.close()
