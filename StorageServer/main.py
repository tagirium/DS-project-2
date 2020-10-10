import os
from StorageServer import StorageServer as sserver
from threading import Thread


def main():
    ss = sserver.StorageServer()
    conn, sock = ss.establish_connection()
    cmd = ss.receive_str(conn)
    if cmd == 'init':
        ss.init(conn)
    elif cmd == 'file_read':
        ss.file_read(ss.receive_str(conn), conn)
    elif cmd == 'file_create':
        ss.file_write(ss.receive_str(conn), conn)
    elif cmd == 'file_delete':
        ss.file_delete(ss.receive_str(conn), conn)
    elif cmd == 'file_info':
        ss.file_info(ss.receive_str(conn), conn)
    elif cmd == 'file_copy':
        paths= ss.receive_str(conn).split('||')
        ss.file_copy(src_path=paths[0], dest_path=paths[1], conn=conn)
    elif cmd == 'file_move':
        paths = ss.receive_str(conn).split('||')
        ss.file_move(src_path=paths[0], dest_path=paths[1], conn=conn)
    elif cmd == 'dir_make':
        ss.dir_make(path=ss.receive_str(conn), conn=conn)
    elif cmd == 'dir_delete':
        ss.dir_delete(path=ss.receive_str(conn), conn=conn)
    elif cmd == 'time_to_die':
        ss.close_connection(sock)
    else:
        print('Invalid command')


if __name__ == '__main__':
    thread = Thread(target=sserver.ping_from_naming(), daemon=True)
    thread.start()
    while True:
        main()

