import socket
import os

BUFFER_SIZE = 2048
CODE_OK = 4

# print("Enter Naming Server's IP: ")
NAMING_SERVER_IP = "192.168.43.117"
# NAMING_SERVER_IP = input()
PORT = 8080

# Create socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((NAMING_SERVER_IP, PORT))


def send(cmd, p):
    s.send(cmd.encode())
    s.send(p.encode())

    if cmd == 'file_write':
        print("Enter path of a file u want to send: ")
        filepath = input()

        if os.path.exists(filepath):
            s.send(str(os.stat(filepath).st_size).encode())

        # Send the file data
        with open(filepath, 'rb') as fa:
            num_of_blocks = os.stat(filepath).st_size//BUFFER_SIZE
            for i in range(num_of_blocks):
                data = fa.read(BUFFER_SIZE)
                # print(data)
                s.send(data)
            final_data = fa.read(os.stat(filepath).st_size - num_of_blocks * BUFFER_SIZE)
            # print(final_data)
            s.send(final_data)
            fa.close()


def receive(sock):
    string = ''
    # Receive, output and save file
    while True:
        data = sock.recv(BUFFER_SIZE)
        string += data.decode()
        break

    return string


def receive_file(sock, fname):
    # Receive, output and save file
    st = receive(s)
    filesize = int(st)
    with open(fname, "wb") as fw:
        for i in range(filesize):
            data = sock.recv(1)
            fw.write(data)
            fw.flush()
        fw.close()


while True:

    print("Enter command: ")
    command = input()

    if command == 'init':
        s.send(command.encode())
        output = s.recv(BUFFER_SIZE)
        print(output)

    elif command == 'file_create':
        print("Enter path: ")
        path = input()
        send(command, path)

    elif command == 'file_read':
        print("Enter path: ")
        path = input()
        send(command, path)
        filename = os.getcwd() + '/' + path.split('/')[len(path.split())]
        receive_file(s, filename)

    elif command == 'file_write':
        print("Enter path: ")
        path = input()
        send(command, path)

    elif command == 'file_delete':
        print("Enter path: ")
        path = input()
        send(command, path)

    elif command == 'file_info':
        print("Enter path: ")
        path = input()
        send(command, path)
        output = receive(s)
        print("File info:", output)

    elif command == 'file_copy':
        print("Enter path: ")
        path = input()
        print("Enter destination path: ")
        path_dest = input()
        path_new = path+'||'+path_dest
        send(command, path_new)

    elif command == 'file_move':
        print("Enter path: ")
        path = input()
        print("Enter destination path: ")
        path_dest = input()
        path_new = path + '||' + path_dest
        send(command, path_new)

    elif command == 'dir_open':
        print("Enter path: ")
        path = input()
        send(command, path)

    elif command == 'dir_read':
        print("Enter path: ")
        path = input()
        send(command, path)
        output = receive(s)
        print("File information: ", output)

    elif command == 'dir_make':
        print("Enter path: ")
        path = input()
        send(command, path)

    elif command == 'dir_delete':
        print("Enter path: ")
        path = input()
        send(command, path)

    else:
        print("Invalid command. You can only use following commands:\n init\n file_create\n file_read\n file_write\n "
              "file_delete\n file_info\n file_copy\n file_move\n dir_open\n dir_read\n dir_make\n dir_delete")

    # if that's it:
    print("If that's it send command 'quit', otherwise press Enter")
    quit_cmd = input()
    if quit_cmd == 'quit':
        ttd = 'time_to_die'
        s.send(ttd.encode())
        break
