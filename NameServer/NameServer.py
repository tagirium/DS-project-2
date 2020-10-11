import socket
from .codes import *
from threading import Thread
import time
import os


class Directory(object):

    def __init__(self, name):
        self.list = []
        self.name = name
        self.prev = None

    def add_child(self, obj):
        obj.prev = self
        self.list.append(obj)

    def print_children(self):
        for i in range(len(self.list)):
            print('/ ', self.list[i].name)

    def find_by_name(self, name):
        if name == '/':
            return self
        for i in range(len(self.list)):
            if self.list[i].name == name:
                return self.list[i]
        return None

    def add_file_to_path(self, path):
        dirs = []
        dirs = path.split('/')
        dirs[0] = '/'
        name = dirs[len(dirs) - 1]
        dirs.pop()
        depth = len(dirs) - 1
        dir = self
        if depth == 0:
            dir.add_child(File(name))
            return
        for i in range(depth):
            dir = dir.find_by_name(dirs[i + 1])
        dir.add_child(File(name))

    def add_directory_to_path(self, path):
        dirs = []
        dirs = path.split('/')
        dirs[0] = '/'
        name = dirs[len(dirs) - 1]
        dirs.pop()
        depth = len(dirs) - 1
        dir = self
        if depth == 0:
            dir.add_child(Directory(name))
            return
        for i in range(depth):
            dir = dir.find_by_name(dirs[i + 1])
        dir.add_child(Directory(name))

    def remove_from_path(self, path):
        dirs = []
        dirs = path.split('/')
        dirs[0] = '/'
        name = dirs[len(dirs) - 1]
        dirs.pop()
        depth = len(dirs) - 1
        dir = self

        if depth == 0:
            for i in range(len(dir.list)):
                if dir.list[i].name == name:
                    dir.list.pop(i)
                    return 0
        for i in range(depth):
            dir = dir.find_by_name(dirs[i + 1])

        for i in range(len(dir.list)):
            if dir.list[i].name == name:
                dir.list.pop(i)
                # print('deleted')
                return 0
        return 1

    def get_from_path(self, path):
        path = path + '/'
        dirs = []
        dirs = path.split('/')
        dirs[0] = '/'
        name = dirs[len(dirs) - 1]
        dirs.pop()
        depth = len(dirs) - 1
        dir = self
        print(dirs)
        if depth == 0:
            return dir
        for i in range(depth):
            dir = dir.find_by_name(dirs[i + 1])
        return dir

    def get_directory(self, path):
        contents = ''
        dir = self.get_from_path(path)
        for i in range(len(dir.list)):
            contents = contents + dir.list[i].name + '/'
        return contents

    def go_to_root(self):
        dir = self
        while dir.name != '/':
            dir = self.prev
        return dir


class File(object):

    def __init__(self, name):
        self.name = name
        self.prev = None


def initialize():
    directory_tree = Directory('/')
    return directory_tree


def file_create(root: Directory, path):
    root.add_file_to_path(path)
    return


def file_delete(root: Directory, path):
    root.remove_from_path(path)
    return


def file_copy(root: Directory, path1, path2):
    name = root.get_from_path(path1).name
    path2 = path2 + '/' + name
    root.add_file_to_path(path2)


def file_move(root: Directory, path1, path2):
    name = root.get_from_path(path1).name
    root.remove_from_path(path1)
    path2 = path2 + '/' + name
    root.add_file_to_path(path2)


def establish_connection(port):
    ns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ns.bind((socket.gethostname(), port))
    ns.listen()
    (conn, address) = ns.accept()
    return conn, ns


def send_response(code: int, conn):
    conn.send(code.to_bytes(32, 'big'))


def receive_str(conn):
    string = ''
    # Receive, output and save file
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        else:
            string += data.decode()
    send_response(CODE_OK, conn)
    return string


def receive_file(conn):
    text_file = './file'
    # Receive, output and save file
    with open(text_file, "wb") as fw:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            else:
                fw.write(data)
    send_response(CODE_OK, conn)


def send_string(ns, string):
    ns.send(string.encode())


def send_file(ns):
    filepath = './file'

    # Send the file data
    with open(filepath, 'ab+') as fa:
        l = fa.read(BUFFER_SIZE)
        while l:
            ns.send(l)
            flag = ns.recv(BUFFER_SIZE)
            if flag != CODE_OK:
                print("Error")
                exit()
            l = fa.read(BUFFER_SIZE)
        fa.close()


active_storages = {'ip1': [], 'ip2': [], 'ip3': []}
storages = ['ip1', 'ip2', 'ip3']

j = 0
sns = []
for i in storages:
    active_storages[i].append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    active_storages[i].append(time.time())
    active_storages[i][0].connect((i, STORAGE_SERVER_PORT))


def check_storages():
    chk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        data, (ip, port) = chk.recvfrom(BUFFER_SIZE)
        time_now = time.time()
        active_storages[ip][1] = time_now
        for ips in list(active_storages.keys()):
            if time_now - active_storages[ips][1] > 10:
                active_storages.pop(ips)


work_dir = None
thread = Thread(target=check_storages(), daemon=True)
thread.start()

addr = ''
conn, sock = establish_connection()

while True:

    command = receive_str()

    if command == 'initialize':

        work_dir = initialize()
        active = active_storages[list(active_storages.keys())[0]][0]
        b = True
        for i in active_storages.keys():
            send_string(active_storages[i][0], command)
            if b:
                send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)
                b = False
            else:
                active_storages[i][0].recv(BUFFER_SIZE)

    elif command == 'file_create':
        path = receive_str(conn)
        file_create(work_dir, path)
        active = active_storages[list(active_storages.keys())[0]][0]
        for i in active_storages.keys():
            send_string(active_storages[i][0], command)
            send_string(active_storages[i][0], path)
            if b:
                send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)
                b = False
            else:
                active_storages[i][0].recv(BUFFER_SIZE)

    elif command == 'file_read':
        path = receive_str(conn)
        active = active_storages[list(active_storages.keys())[0]][0]
        send_string(active, command)
        send_string(active, path)
        send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)

        receive_file(active)
        send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)

        send_file(conn)

    elif command == 'file_write':
        path = receive_str(conn)
        receive_file(conn)

        active = active_storages[list(active_storages.keys())[0]][0]
        b = True
        c = True
        for i in active_storages.keys():
            send_string(active_storages[i][0], command)
            send_string(active_storages[i][0], path)

            if b:
                send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)
                b = False
            else:
                active_storages[i][0].recv(BUFFER_SIZE)

            send_file(active_storages[i][0])

            if c:
                send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)
                c = False
            else:
                active_storages[i][0].recv(BUFFER_SIZE)

        file_create(work_dir, path)

    elif command == 'file_delete':
        path = receive_str(conn)
        file_delete(work_dir, path)
        b = True
        active = active_storages[list(active_storages.keys())[0]][0]
        for i in active_storages.keys():
            send_string(active_storages[i][0], command)
            send_string(active_storages[i][0], path)
            if b:
                send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)
                b = False
            else:
                active_storages[i][0].recv(BUFFER_SIZE)
            active_storages[i][0].recv(BUFFER_SIZE)
        send_response(int.from_bytes(sns.recv(BUFFER_SIZE), byteorder='big'), conn)
        print('done')

    elif command == 'file_info':
        path = receive_str(conn)
        send_string(sns, path)
        send_response(int.from_bytes(sns.recv(BUFFER_SIZE), byteorder='big'), conn)
        info = receive_str(sns)
        send_response(int.from_bytes(sns.recv(BUFFER_SIZE), byteorder='big'), conn)
        send_string(conn, info)
        print('done')

    elif command == 'file_copy':
        paths = receive_str(conn)
        path = paths.split('||')
        file_copy(work_dir, path[0], path[1])
        send_string(sns, command)
        send_string(sns, paths)
        send_response(int.from_bytes(sns.recv(BUFFER_SIZE), byteorder='big'), conn)
        print('done')

    elif command == 'file_move':
        paths = receive_str(conn)
        path = paths.split('||')
        file_move(work_dir, path[0], path[1])
        send_string(sns, command)
        send_string(sns, paths)
        send_response(int.from_bytes(sns.recv(BUFFER_SIZE), byteorder='big'), conn)
        print('done')

    elif command == 'open_directory':
        path = receive_str(conn)
        print('done')
    elif command == 'read_directory':
        path = receive_str(conn)
        direct = work_dir.get_directory(path)
        send_string(conn, direct)
        print('done')
    elif command == 'make_directory':
        path = receive_str(conn)
        work_dir.add_directory_to_path(path)
        send_string(sns, command)
        send_string(sns, path)
        send_response(int.from_bytes(sns.recv(BUFFER_SIZE), byteorder='big'), conn)
        print('done')
    elif command == 'delete_directory':
        path = receive_str(conn)
        work_dir.remove_from_path(path)
        send_string(sns, command)
        send_string(sns, path)
        print('done')
    elif command == 'time_to_die':
        conn.close()
        send_string(sns, command)

    str_from_client = 'file_create||/a.txt||'
    # TODO Do operations on dir tree
    # TODO Send instructions and files to storage servers
