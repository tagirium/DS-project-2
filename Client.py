import socket

BUFFER_SIZE = 32
CODE_OK = 4

print("Enter Naming Server's IP: ")
NAMING_SERVER_IP = input()
PORT = 8880

# Create socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((NAMING_SERVER_IP, PORT))


def send(cmd, p):
    s.send(cmd.encode())
    s.send(p.encode())

    flag = s.recv(BUFFER_SIZE)
    if flag != CODE_OK:
        print("Wrong path")
        exit()

    if command == 'file_write':
        print("Enter path of a file u want to send: ")
        filepath = input()

        # Send the file data
        with open(filepath, 'ab+') as fa:
            l = fa.read(BUFFER_SIZE)
            while l:
                s.send(l)
                flag = s.recv(BUFFER_SIZE)
                if flag != CODE_OK:
                    print("Error")
                    exit()
                l = fa.read(BUFFER_SIZE)
            fa.close()


def receive(sock):
    string = ''
    # Receive, output and save file
    while True:
        data = sock.recv(BUFFER_SIZE)
        if not data:
            break
        else:
            string += data.decode()
    return string


def receive_file(sock, fname):
    # Receive, output and save file
    with open(fname, "wb") as fw:
        while True:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                break
            else:
                fw.write(data)


print("Enter command: ")
command = input()
print("Enter path: ")
path = input()

while True:
    if command == 'init':
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((NAMING_SERVER_IP, PORT))
        s.send(command.encode())
        # Close the socket to end the connection
        s.close()

    elif command == 'file_create':
        send(command, path)

    elif command == 'file_read':
        send(command, path)
        filename = path.split('/')[len(path.split())-1]
        receive_file(s, filename)

    elif command == 'file_write':
        send(command, path)

    elif command == 'file_delete':
        send(command, path)

    elif command == 'file_info':
        send(command, path)
        output = receive(s)
        print("File info:", output)

    elif command == 'file_copy':
        print("Enter destination path: ")
        path_dest = input()
        path_new = path+'||'+path_dest
        send(command, path_new)

    elif command == 'file_move':
        print("Enter destination path: ")
        path_dest = input()
        path_new = path + '||' + path_dest
        send(command, path_new)

    elif command == 'dir_open':
        send(command, path)

    elif command == 'dir_read':
        send(command, path)
        output = receive(s)
        print("File info:", output)

    elif command == 'dir_make':
        send(command, path)

    elif command == 'dir_delete':
        send(command, path)

    else:
        print("Invalid command. You can only use following commands:\n init\n file_create\n file_read\n file_write\n "
              "file_delete\n file_info\n file_copy\n file_move\n dir_open\n dir_read\n dir_make\n dir_delete")

    # if that's it:
    print("If that's it send command 'quit' ")
    quit_cmd = input()
    if quit_cmd == 'quit':
        ttd = 'time_to_die'
        s.send(ttd.encode())
        break
