from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname
import threading
import configparser
from os import path

PORT = 44460
IDENTIFIER = 'advanced_agriculture:'

config = configparser.RawConfigParser()
config.read(path.join(path.dirname(__file__), '../EnvironmentHandler.cfg'))
announce_interval = config.get('Announce', 'interval')


class Announcer(object):

    def __init__(self):
        self.interval = int(announce_interval)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(('', 0))
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.ip = gethostbyname(gethostname())
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            data = IDENTIFIER + self.ip
            self.socket.sendto(data.encode('utf-8'), ('<broadcast>', PORT))
            sleep(self.interval)
