import socket
import os
from threading import Thread
import time

BUFFER_SIZE = 2048
INITIAL_SIZE = 1024
NAMING_SERVER_IP = "localhost"
STORAGE_SERVER_PORT = 8801
PING_SERVERS_SECONDS = 20
NAMING_SERVER_PORT = 8800  # 555-35-35
# Codes

ERR_PATH_NOT_CORRECT = 1
ERR_FILE_DIR_NOT_EXIST = 2
ERR_DIR_EXISTS = 20
ERR_FILE_EXISTS = 21
CODE_OK = 4


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

        for i in range(depth):
            dir = dir.find_by_name(dirs[i + 1])
            print(name)
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
            contents = contents + ' ' + dir.list[i].name
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


def directory_create(root: Directory, path):
    root.add_directory_to_path(path)
    return


def file_delete(root: Directory, path):
    root.remove_from_path(path)
    return


def directory_delete(root: Directory, path):
    root.remove_from_path(path)
    return


def file_copy(root: Directory, path1, path2):
    root.add_file_to_path(path2)


def file_move(root: Directory, path1, path2):
    root.remove_from_path(path1)
    root.add_file_to_path(path2)


def establish_connection(port):
    ns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ns.bind(('192.168.43.117', port))
    ns.listen()
    (conn, address) = ns.accept()
    return conn, ns


def send_response(code: int, conn):
    conn.send(code.to_bytes(32, 'big'))


def receive_str(conn):
    string = ''
    # Receive, output and save file
    while True:
        data = conn.recv(2048)
        print(data)
        string += data.decode()
        break
        # print(type(string))
    # send_response(CODE_OK, conn)
    return string


def receive_file(conn, size):
    text_file = 'file'  # path
    # Receive, output and save file
    fw = open(text_file, "wb")
    kek = ''
    for i in range(size):
        data = conn.recv(1)
        fw.write(data)
        fw.flush()
    fw.close()


def send_file(conn):
    path = 'file'

    if os.path.exists(path):
        with open(path, 'rb') as fa:
            num_of_blocks = os.stat(path).st_size // BUFFER_SIZE
            for i in range(num_of_blocks):
                data = fa.read(BUFFER_SIZE)
                conn.send(data)
            final_data = fa.read(os.stat(path).st_size - num_of_blocks * BUFFER_SIZE)
            conn.send(final_data)
    time.sleep(1)


def send_string(ns, string):
    ns.send(string.encode())
    time.sleep(1)


active_storages = {'192.168.43.85': []}
storages = ['192.168.43.85']

j = 0
sns = []
for i in storages:
    active_storages[i].append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    active_storages[i].append(time.time())
    print(active_storages[i][0])
    active_storages[i][0].connect((i, STORAGE_SERVER_PORT))


def check_storages():
    chk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        data, (ip, port) = chk.recvfrom(1024)
        time_now = time.time()
        active_storages[ip][1] = time_now
        for ips in list(active_storages.keys()):
            if time_now - active_storages[ips][1] > 10:
                active_storages.pop(ips)


work_dir = None
# thread = Thread(target=check_storages(), daemon=True)
# thread.start()

addr = ''
conn, sock = establish_connection(8080)

while True:

    command = receive_str(conn)

    if command == 'init':
        print('a')
        work_dir = initialize()
        active = active_storages[list(active_storages.keys())[0]][0]
        b = True
        for i in active_storages.keys():
            send_string(active_storages[i][0], command)
            if b:
                # send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)
                b = False
            # else:
            # active_storages[i][0].recv(BUFFER_SIZE)
        kek = receive_str(active)
        send_string(conn, kek)

    elif command == 'file_create':
        path = receive_str(conn)
        file_create(work_dir, path)
        active = active_storages[list(active_storages.keys())[0]][0]
        b = True
        for i in active_storages.keys():
            send_string(active_storages[i][0], command)
            send_string(active_storages[i][0], path)
            if b:
                # send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)
                b = False
            # else:
            # active_storages[i][0].recv(BUFFER_SIZE)

    elif command == 'file_read':
        path = receive_str(conn)
        active = active_storages[list(active_storages.keys())[0]][0]
        send_string(active, command)
        send_string(active, path)
        # send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)
        size = receive_str(active)
        receive_file(active, int(size))
        send_string(conn, size)
        # send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)

        send_file(conn)

    elif command == 'file_write':
        path = receive_str(conn)
        size = receive_str(conn)
        receive_file(conn, int(size))

        active = active_storages[list(active_storages.keys())[0]][0]
        b = True
        c = True
        for i in active_storages.keys():
            send_string(active_storages[i][0], command)
            send_string(active_storages[i][0], path)
            send_string(active_storages[i][0], size)

            if b:
                # send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)
                b = False
            # else:
            # active_storages[i][0].recv(BUFFER_SIZE)

            send_file(active_storages[i][0])

            if c:
                # send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)
                c = False
            # else:
            # active_storages[i][0].recv(BUFFER_SIZE)

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
                # send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)
                b = False
            # else:
            # active_storages[i][0].recv(BUFFER_SIZE)
            # active_storages[i][0].recv(BUFFER_SIZE)
        # send_response(int.from_bytes(sns.recv(BUFFER_SIZE), byteorder='big'), conn)
        print('done')

    elif command == 'file_info':
        path = receive_str(conn)
        active = active_storages[list(active_storages.keys())[0]][0]
        send_string(active, command)
        send_string(active, path)
        # send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)

        kek = receive_str(active)
        # send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)

        send_string(conn, kek)

    elif command == 'file_copy':

        paths = receive_str(conn)

        active = active_storages[list(active_storages.keys())[0]][0]
        b = True
        c = True
        for i in active_storages.keys():
            send_string(active_storages[i][0], command)
            send_string(active_storages[i][0], paths)

            if b:
                # send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)
                b = False
            # else:
            # active_storages[i][0].recv(BUFFER_SIZE)

        path = paths.split('||')

        file_copy(work_dir, path[0], path[1])

    elif command == 'file_move':
        paths = receive_str(conn)

        active = active_storages[list(active_storages.keys())[0]][0]
        b = True
        c = True
        for i in active_storages.keys():
            send_string(active_storages[i][0], command)
            send_string(active_storages[i][0], paths)

            if b:
                # send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)
                b = False
            # else:
            # active_storages[i][0].recv(BUFFER_SIZE)

        path = paths.split('||')

        file_move(work_dir, path[0], path[1])

    elif command == 'open_directory':
        path = receive_str(conn)
        print('done')

    elif command == 'dir_read':
        path = receive_str(conn)
        direct = work_dir.get_directory(path)
        send_string(conn, direct)
        print('done')

    elif command == 'dir_make':
        path = receive_str(conn)
        directory_create(work_dir, path)
        active = active_storages[list(active_storages.keys())[0]][0]
        b = True
        for i in active_storages.keys():
            send_string(active_storages[i][0], command)
            send_string(active_storages[i][0], path)
            if b:
                # send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)
                b = False
            # else:
            # active_storages[i][0].recv(BUFFER_SIZE)
    elif command == 'dir_delete':
        path = receive_str(conn)
        active = active_storages[list(active_storages.keys())[0]][0]
        directory_delete(work_dir, path)
        b = True
        for i in active_storages.keys():
            send_string(active_storages[i][0], command)
            send_string(active_storages[i][0], path)
            if b:
                # send_response(int.from_bytes(active.recv(BUFFER_SIZE), byteorder='big'), conn)
                b = False
            # else:
            # active_storages[i][0].recv(BUFFER_SIZE)
    elif command == 'time_to_die':
        conn.close()
        # for i in active_storages.keys():
        #   send_string(active_storages[i][0], command)

    try:
        os.remove('file')
    except:
        pass

    # TODO Do operations on dir tree
    # TODO Send instructions and files to storage servers
