import socket
import os
import StorageServer as sserver

def receive_command():
	ssFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ssFT.bind((socket.gethostname(), 8755))
	ssFT.listen(1)
	cmd_string = ''
	while True:
		(conn, address) = ssFT.accept()
		# Receive, output and save file
		while True:
			data = conn.recv(32)
			if not data:
				break
			else:
				cmd_string += data.decode()
		break
	ssFT.close()
	return cmd_string


def send_file(path):
	ssFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ssFT.bind((socket.gethostname(), 8758))
	ssFT.listen(1)
	while True:
		(conn, address) = ssFT.accept()
		with open(path, 'ab+') as fa:
			l = fa.read(32)
			while l:
				conn.send(l)
				l = fa.read(32)
			fa.close()
		break
	ssFT.close()


def main():
	res = receive_command()
	ss = sserver.StorageServer()
	if res == 'file_read':
		ss.file_read(path=ss.receive_path())
	elif res == 'file_create':
		ss.file_write(path=ss.receive_path())
	elif res == 'file_delete':
		ss.file_delete(path=ss.receive_path())
	elif res == 'file_info':
		ss.file_info(path=ss.receive_path())
	elif res == 'file_copy':
		ss.file_copy(src_path=ss.receive_path(), dest_path=ss.receive_path())
	elif res == 'dir_open':
		ss.dir_open(path=ss.receive_path())
	elif res == 'dir_read':
		f = open('response.txt', 'w')
		f.write(ss.dir_read(path=ss.receive_path()))
		f.close()
		send_file('response.txt')
		os.remove('response.txt')
	elif res == 'dir_make':
		ss.dir_make(path=ss.receive_path())
	elif res == 'dir_delete':
		ss.dir_delete(path=ss.receive_path())
	else:
		print('Invalid command')


if __name__ == '__main__':
	while True:
		main()
