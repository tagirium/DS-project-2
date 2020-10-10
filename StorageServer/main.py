import os
from StorageServer import StorageServer as sserver
from StorageServer.codes import *
from threading import Thread

def main():
    ss = sserver.StorageServer()
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
    else:
        print('Invalid command')


if __name__ == '__main__':
    if not os.path.exists(STORAGE_SERVER_ROOT_PATH):
        os.mkdir(STORAGE_SERVER_ROOT_PATH)
    thread = Thread(target=sserver.ping_from_naming(), daemon=True)
    thread.start()
    while True:
        main()

