import socket
from .codes import *
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
                    print('deleted')
                    return 0
                else:
                    print('not this one')
        for i in range(depth):
            dir = dir.find_by_name(dirs[i + 1])

        for i in range(len(dir.list)):
            if dir.list[i].name == name:
                dir.list.pop(i)
                # print('deleted')
                return 0
            # else:
            # print('not this one')
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

    def go_to_root(self):
        dir = self
        while (dir.name != '/'):
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
    # TODO
    return


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


work_dir = None
while True:
    conn, sock = establish_connection()
    addr = ''
    sns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sns.connect((addr, STORAGE_SERVER_PORT))

    command = receive_str()

    if command == 'initialize':
        work_dir = initialize()
        print('initialized')
    elif command == 'file_create':
        path = receive_str(conn)
        file_create(work_dir, path)
        send_string(sns, command)
        send_string(sns, path)
        send_response(int.from_bytes(sns.recv(BUFFER_SIZE), byteorder='big'), conn)
        work_dir.print_children()
        print('file created')

    elif command == 'file_read':
        path = receive_str(conn)
        send_string(sns, command)
        send_string(sns, path)
        send_response(int.from_bytes(sns.recv(BUFFER_SIZE), byteorder='big'), conn)
        receive_file(sns)
        send_response(int.from_bytes(sns.recv(BUFFER_SIZE), byteorder='big'), conn)
        send_file(conn)
        print('done')

    elif command == 'file_write':
        path = receive_str(conn)
        receive_file(conn)
        send_string(sns, command)
        send_string(sns, path)
        send_response(int.from_bytes(sns.recv(BUFFER_SIZE), byteorder='big'), conn)
        send_file(sns)
        send_response(int.from_bytes(sns.recv(BUFFER_SIZE), byteorder='big'), conn)
        file_create(work_dir, path)
        print('done')

    elif command == 'file_delete':
        path = receive_str(conn)
        # TODO delete
        send_string(sns, command)
        send_string(sns, path)
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
        # TODO file copy
        send_string(sns, command)
        send_string(sns, paths)
        send_response(int.from_bytes(sns.recv(BUFFER_SIZE), byteorder='big'), conn)
        print('done')

    elif command == 'file_move':
        paths = receive_str(conn)
        # TODO file move
        send_string(sns, command)
        send_string(sns, paths)
        send_response(int.from_bytes(sns.recv(BUFFER_SIZE), byteorder='big'), conn)
        print('done')

    elif command == 'open_directory':
        path = receive_str(conn)
        print('done')
    elif command == 'read_directory':
        path = receive_str(conn)
        # TODO read diroctory
        direct = ''
        send_string(conn, direct)
        print('done')
    elif command == 'make_directory':
        path = receive_str(conn)
        #TODO make dir
        send_string(sns,command)
        send_string(sns, path)
        send_response(int.from_bytes(sns.recv(BUFFER_SIZE), byteorder='big'), conn)
        print('done')
    elif command == 'delete_directory':
        path = receive_str(conn)
        #TODO make dir
        send_string(sns, command)
        send_string(sns, path)
        print('done')
    elif command == 'time_to_die':
        conn.close()
        send_string(sns, command)

    str_from_client = 'file_create||/a.txt||'
    # TODO Do operations on dir tree
    # TODO Send instructions and files to storage servers
