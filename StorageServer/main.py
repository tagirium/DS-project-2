from threading import Thread

import shutil
import os
import time
import socket

# Constants
BUFFER_SIZE = 2048
STORAGE_SERVER_ROOT_PATH = "./sserver_files"
NAMING_SERVER_IP = "192.168.43.117"
STORAGE_SERVER_PORT = 8801
PING_SERVERS_SECONDS = 20
NAMING_SERVER_PORT = 8800  # 555-35-35
# Codes

ERR_PATH_NOT_CORRECT = 1
ERR_FILE_DIR_NOT_EXIST = 2
ERR_DIR_EXISTS = 20
ERR_FILE_EXISTS = 21
CODE_OK = 4

class StorageServer:

    def file_read(self, path, conn):
        if os.path.exists(path):
            self.send_file(path, conn)

    def file_create(self, path, conn):
        if True: #self.check_path_correctness(path):
            print('path correct')
            if not os.path.exists(path):
                file = open(path, 'w+')
                file.close()
            else:
                print('path exists')

    def file_write(self, path, conn):
        print(path)
        if not os.path.exists(path):
            print(path + ' 2')
            size = int(self.receive_str(conn))
            self.receive_file(path, conn, size)

    def file_delete(self, path, conn):
        if os.path.exists(path):
            os.remove(path)

    def file_info(self, path, conn):
        if os.path.exists(path):
            res = os.stat(path)
            self.send_string(conn, str(res))

    def file_copy(self, src_path, dest_path, conn):
        if os.path.exists(src_path):
            if not os.path.exists(dest_path):
                if True:#self.check_path_correctness(dest_path):
                    shutil.copyfile(src_path, dest_path)

    def file_move(self, src_path, dest_path, conn):
        if os.path.exists(src_path):
            if not os.path.exists(dest_path):
                if True:#self.check_path_correctness(dest_path):
                    self.file_copy(src_path, dest_path,conn)
                    self.file_delete(src_path, conn)

    def dir_make(self, path, conn):
        if not os.path.exists(path):
            if True:#self.check_path_correctness(path):
                os.mkdir(path)
            pass

    def dir_delete(self, path, conn):
        if os.path.exists(path):
            os.rmdir(path)

    def receive_file(self, path, conn, size):
        text_file = path  # path
        # Receive, output and save file
        fw = open(text_file, "wb")
        for i in range(size):
            data = conn.recv(1)
            fw.write(data)
            fw.flush()
        fw.close()

    def send_file(self, path, conn):
        if os.path.exists(path):
            self.send_string(conn, str(os.stat(path).st_size))
            with open(path, 'rb') as fa:
                num_of_blocks = os.stat(path).st_size // BUFFER_SIZE
                print(num_of_blocks)
                for i in range(num_of_blocks):
                    data = fa.read(BUFFER_SIZE)
                    print(data)
                    conn.send(data)
                final_data = fa.read(os.stat(path).st_size - num_of_blocks * BUFFER_SIZE)
                print(final_data)
                conn.send(final_data)
                fa.close()

    def receive_str(self, conn):
        string = ''
        # Receive, output and save file
        while True:
            data = conn.recv(BUFFER_SIZE)
            string += data.decode()
            break
        return string

    def establish_connection(self):
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.bind(('', STORAGE_SERVER_PORT))
        ss.listen()
        (conn, address) = ss.accept()
        print('connection established, address is', address)
        return conn, ss

    def send_response(self, code: int, conn):
        conn.send(code.to_bytes(32, 'big'))

    # def check_path_correctness(self, path: str):
    #     path_list = path.split('/')
    #     full_path = os.getcwd()
    #     print(path_list)
    #     for directory in path_list[1:len(path) - 2]:
    #         print(full_path)
    #         full_path += '\\' + directory
    #         print(os.path.isdir(full_path))
    #         if not os.path.isdir(full_path):
    #             return False
    #     return True

    def close_connection(self, sock):
        sock.close()

    def init(self, conn):
        print('init started')
        if os.path.exists(STORAGE_SERVER_ROOT_PATH):
            print('removed tree')
            shutil.rmtree(STORAGE_SERVER_ROOT_PATH)
            os.mkdir(STORAGE_SERVER_ROOT_PATH)
        else:
            print('created tree')
            os.mkdir(STORAGE_SERVER_ROOT_PATH)
        self.send_string(string=str(shutil.disk_usage(STORAGE_SERVER_ROOT_PATH).free // 2**30), conn=conn)

    def send_string(self, conn, string):
        conn.send(string.encode())
        time.sleep(1)

    def ping_from_naming(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            sock.sendto(CODE_OK.to_bytes(32, 'big'), (NAMING_SERVER_IP, NAMING_SERVER_PORT))
            time.sleep(10.0)


def main(ss, conn, sock):
    cmd = ss.receive_str(conn)
    print(cmd)
    if cmd == 'init':
        ss.init(conn)
    elif cmd == 'file_read':
        path = STORAGE_SERVER_ROOT_PATH + ss.receive_str(conn)
        print(path)
        ss.file_read(path, conn)
    elif cmd == 'file_write':
        path = STORAGE_SERVER_ROOT_PATH + ss.receive_str(conn)
        print(path)
        ss.file_write(path, conn)
    elif cmd == 'file_create':
        path = STORAGE_SERVER_ROOT_PATH + ss.receive_str(conn)
        print(path)
        ss.file_create(path, conn)
    elif cmd == 'file_delete':
        ss.file_delete(STORAGE_SERVER_ROOT_PATH + ss.receive_str(conn), conn)
    elif cmd == 'file_info':
        ss.file_info(STORAGE_SERVER_ROOT_PATH + ss.receive_str(conn), conn)
    elif cmd == 'file_copy':
        paths= ss.receive_str(conn).split('||')
        ss.file_copy(src_path=STORAGE_SERVER_ROOT_PATH + paths[0], dest_path=STORAGE_SERVER_ROOT_PATH + paths[1], conn=conn)
    elif cmd == 'file_move':
        paths = ss.receive_str(conn).split('||')
        ss.file_move(src_path=STORAGE_SERVER_ROOT_PATH + paths[0], dest_path=STORAGE_SERVER_ROOT_PATH + paths[1], conn=conn)
    elif cmd == 'dir_make':
        ss.dir_make(path=STORAGE_SERVER_ROOT_PATH + ss.receive_str(conn), conn=conn)
    elif cmd == 'dir_delete':
        ss.dir_delete(path=STORAGE_SERVER_ROOT_PATH + ss.receive_str(conn), conn=conn)
    elif cmd == 'time_to_die':
        ss.close_connection(sock)
    else:
        print('Invalid command - ', cmd, '-')


if __name__ == '__main__':
    ss = StorageServer()
    conn, sock = ss.establish_connection()
    #thread = Thread(target=ss.ping_from_naming(), daemon=True)
    #thread.start()
    while True:
        main(ss, conn, sock)

