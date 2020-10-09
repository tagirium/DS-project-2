import socket
import StorageServer as sserver
from codes import *


def main():
    ss = sserver.StorageServer()
    cmd = ss.receive_str
    if cmd == 'file_read':
        ss.file_read(path=ss.receive_str)
    elif cmd == 'file_create':
        ss.file_write(path=ss.receive_str)
    elif cmd == 'file_delete':
        ss.file_delete(path=ss.receive_str)
    elif cmd == 'file_info':
        ss.file_info(path=ss.receive_str)
    elif cmd == 'file_copy':
        ss.file_copy(src_path=ss.receive_str(), dest_path=ss.receive_str())
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
    while True:
        main()

