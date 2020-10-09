import os
from StorageServer import StorageServer as sserver
from StorageServer.codes import *


def main():
    ss = sserver.StorageServer(8800)  # 555-35-35
    cmd = ss.receive_str()
    if cmd == 'file_read':
        ss.file_read(path=ss.receive_str())
    elif cmd == 'file_create':
        ss.file_write(path=ss.receive_str())
    elif cmd == 'file_delete':
        ss.file_delete(path=ss.receive_str())
    elif cmd == 'file_info':
        res = ss.file_info(path=ss.receive_str())
        if res != -1:
            f = open('response.txt', 'w')
            f.write(res)
            f.close()
            ss.send_file('response.txt')
            os.remove('response.txt')
    elif cmd == 'file_copy':
        paths = ss.receive_str().split('||')
        ss.file_copy(src_path=paths[0], dest_path=paths[1])
    elif cmd == 'file_move':
        paths = ss.receive_str().split('||')
        ss.file_move(src_path=paths[0], dest_path=paths[1])
    elif cmd == 'dir_open':
        ss.dir_open(path=ss.receive_str())
    elif cmd == 'dir_read':
        f = open('response.txt', 'w')
        f.write(ss.dir_read(path=ss.receive_str()))
        f.close()
        ss.send_file('response.txt')
        os.remove('response.txt')
    elif cmd == 'dir_make':
        ss.dir_make(path=ss.receive_str())
    elif cmd == 'dir_delete':
        ss.dir_delete(path=ss.receive_str())
    elif cmd == 'ping_from_naming':
        ss.ping_from_naming()
    else:
        print('Invalid command')


if __name__ == '__main__':
    if not os.path.exists(STORAGE_SERVER_ROOT_PATH):
        os.mkdir(STORAGE_SERVER_ROOT_PATH)
    while True:
        main()

