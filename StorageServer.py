import os
import shutil
from help import *
from codes import *


class StorageServer:
	def file_read(self, path):
		self.send_file(path)

	def file_create(self, path):
		file = open(path, 'w+')
		file.close()

	def file_write(self, path):
		self.receive_file(path)

	def file_delete(self, path):
		if os.path.exists(path):
			os.remove(path)

	def file_info(self, path):
		if os.path.exists(path):
			return os.stat(path)

	def file_copy(self, src_path, dest_path):
		shutil.copyfile(src_path, dest_path)

	def file_move(self, src_path, dest_path):
		self.file_copy(src_path, dest_path)
		self.file_delete(src_path)

	def dir_open(self, path):
		if os.path.exists(path):
			os.chdir(path)

	def dir_read(self, path):
		if os.path.exists(path) and os.path.isdir(path):
			entries = os.listdir(path)
			return ' '.join(list(map(str, entries)))

	def dir_make(self, path):
		if not os.path.exists(path):
			os.mkdir(path)

	def dir_delete(self, path):
		if os.path.exists(path):
			os.rmdir(path)

	def receive_file(self, path):
		ssFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ssFT.bind((socket.gethostname(), 8801))
		ssFT.listen(1)
		while True:
			(conn, address) = ssFT.accept()
			text_file = path  # path

			# Receive, output and save file
			with open(text_file, "wb") as fw:
				while True:
					data = conn.recv(BUFFER_SIZE)
					if not data:
						break
					else:
						fw.write(data)

			break
		ssFT.close()

	def send_file(self, path):
		ssFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ssFT.bind((socket.gethostname(), STORAGE_SERVER_PORT))
		ssFT.listen(1)
		while True:
			(conn, address) = ssFT.accept()
			with open(path, 'ab+') as fa:
				l = fa.read(BUFFER_SIZE)
				while l:
					conn.send(l)
					l = fa.read(BUFFER_SIZE)
				fa.close()
			break
		ssFT.close()

	def receive_path(self):
		ssFT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ssFT.bind((socket.gethostname(), STORAGE_SERVER_PORT))
		ssFT.listen(1)
		path = ''  # path
		while True:
			(conn, address) = ssFT.accept()
			# Receive, output and save file
			while True:
				data = conn.recv(BUFFER_SIZE)
				if not data:
					break
				else:
					path += data.decode()
			break
		ssFT.close()
		return path

