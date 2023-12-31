"""
cloud_storage
Author:LXQing
Date:2023/08/22
"""

import struct
from socket import *
import os


class Server:
    def __init__(self, ip, port):
        # 添加注解要在Init位置
        self.s_listen: socket = None  # 用来listen的socket对象
        self.ip = ip
        self.port = port

    def tcp_init(self):
        self.s_listen = socket(AF_INET, SOCK_STREAM)
        self.s_listen.bind((self.ip, self.port))
        self.s_listen.listen(128)
        # return self.s_listen

    def task(self):
        new_client, client_add = self.s_listen.accept()
        user = User(new_client)
        user.deal_command()  # 处理客户端发过来的各种命令


class User:
    '''
    每一个user对象对应一个客户端
    '''

    def __init__(self, new_client):
        self.new_client: socket = new_client
        self.user_name = None
        self.path = os.getcwd()  # 存储连上的用户路径

    def deal_command(self):
        while True:
            command = self.recv_train().decode('utf8')
            if command[:2] == 'ls':
                self.do_ls()
            elif command[:2] == 'cd':
                self.do_cd(command)
            elif command[:3] == 'pwd':
                self.do_pwd()
            elif command[:2] == 'rm':
                self.do_rm(command)
            elif command[:4] == 'gets':
                self.do_gets(command)
            elif command[:4] == 'puts':
                self.do_puts(command)
            else:
                print('Wrong command')

    def send_train(self, send_bytes):
        '''开火车，就是把某个字节流内容以火车流的从事发过去'''
        train_head_bytes = struct.pack('I', len(send_bytes))
        self.new_client.send(train_head_bytes + send_bytes)

    def recv_train(self):
        '''
        recv火车，就是把火车接收的内容返回回去
        :return:
        '''
        train_head_bytes = self.new_client.recv(4)
        # print(len(train_head_bytes))
        train_head = struct.unpack('I', train_head_bytes)
        return self.new_client.recv(train_head[0])

    def do_ls(self):
        data = ''
        for file in os.listdir(self.path):
            data += file + ' ' * 5 + str(os.stat(file).st_size) + '\n'
        self.send_train(data.encode('utf8'))

    def do_cd(self,command):
        path=command.split()[1]
        os.chdir(path)
        self.path=os.getcwd()
        self.send_train(self.path.encode('utf8'))  # 每次客户端执行后显示路径

    def do_pwd(self):
        self.send_train(self.path.encode('utf8'))

    def do_rm(self,command):
        pass
    def do_gets(self,command):
        pass

if __name__ == '__main__':
    server = Server('192.168.31.67', 2000)
    server.tcp_init()
    server.task()
