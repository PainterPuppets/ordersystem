#coding:utf-8

from socket import AF_INET, SOCK_STREAM, socket

class Client(object):
    def __init__(self, port):
        self.port = port

    def establish(self):
        self.cs = socket(AF_INET, SOCK_STREAM)


    def connect(self):
        self.cs.connect(self.port)
        

    def close(self):
        self.cs.close()


    def dialogue(self):
        while True:
            self.establish()
            print '建立socket成功！！！'
            self.connect()
            print '连接服务器成功！！！'
            f = self.cs.makefile(bufsize=1)
            s = raw_input('请输入指令:')
            f.write(s+'\n')
            print f.readline()
            self.close()


client = Client(('10.42.0.1', 8889))
client.dialogue()
