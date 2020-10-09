import socket
import StorageServer as sserver
from codes import *
import time


def open_socket(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # sock.settimeout(10) # make longer for large uploads
        sock.connect((ip, port))
        return sock
    except Exception as e:
        print('Can not open connection to ' + ip + ':' + str(port))
        return False


def ping_naming_server(self):
    print('Attempting to contact naming server.')
    naming_server_sock = open_socket(NAMING_SERVER_IP, NAMING_SERVER_PORT)
    while not naming_server_sock:
        print('Could not connect to naming server. Pining again after 20 seconds.')
        time.sleep(20)
        naming_server_sock = open_socket(NAMING_SERVER_IP, NAMING_SERVER_PORT)
    print('Connected to naming server!')
    naming_server_sock.send(CMD_PING_FROM_STORAGE.to_bytes())
    ret = int.from_bytes(naming_server_sock.recv(32))
    if ret != CODE_OK:
        print('Naming server sending wrong code at init.')
        return False
    return True


def receive_command():
    ssFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssFT.bind((socket.gethostname(), NAMING_SERVER_PORT))
    ssFT.listen(1)
    cmd_string = ''
    while True:
        (conn, address) = ssFT.accept()
        # Receive, output and save file
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            else:
                cmd_string += data.decode()
        break
    ssFT.close()
    return cmd_string


def ping_from_naming():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((socket.gethostname(), NAMING_SERVER_PORT))
    sock.send(CODE_OK.to_bytes())

def main():
    cmd = receive_command()
    ss = sserver.StorageServer()
    if cmd == 'file_read':
        ss.file_read(path=ss.receive_path())
    elif cmd == 'file_create':
        ss.file_write(path=ss.receive_path())
    elif cmd == 'file_delete':
        ss.file_delete(path=ss.receive_path())
    elif cmd == 'file_info':
        ss.file_info(path=ss.receive_path())
    elif cmd == 'file_copy':
        ss.file_copy(src_path=ss.receive_path(), dest_path=ss.receive_path())
    elif cmd == 'dir_open':
        ss.dir_open(path=ss.receive_path())
    elif cmd == 'dir_read':
        f = open('response.txt', 'w')
        f.write(ss.dir_read(path=ss.receive_path()))
        f.close()
        ss.send_file('response.txt')
        os.remove('response.txt')
    elif cmd == 'dir_make':
        ss.dir_make(path=ss.receive_path())
    elif cmd == 'dir_delete':
        ss.dir_delete(path=ss.receive_path())
    elif cmd == 'ping_from_naming':
        ping_from_naming()
    else:
        print('Invalid command')


if __name__ == '__main__':
    while True:
        main()

