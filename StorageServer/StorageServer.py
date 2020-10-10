import shutil
import os
from StorageServer.codes import *
import socket


class StorageServer:

	def file_read(self, path, conn):
		if os.path.exists(path):
			self.send_file(path, conn)
			self.send_response(CODE_OK, conn)
		else:
			self.send_response(ERR_PATH_NOT_CORRECT, conn)

	def file_create(self, path, conn):
		if self.check_path_correctness(path):
			if not os.path.exists(path):
				file = open(path, 'w+')
				file.close()
				self.send_response(CODE_OK, conn)
			else:
				self.send_response(ERR_FILE_EXISTS, conn)
		else:
			self.send_response(ERR_PATH_NOT_CORRECT, conn)

	def file_write(self, path, conn):
		if not os.path.exists(path):
			if self.check_path_correctness(path):
				self.receive_file(path, conn)
				self.send_response(CODE_OK, conn)
			else:
				self.send_response(ERR_PATH_NOT_CORRECT, conn)
		else:
			self.send_response(ERR_FILE_EXISTS, conn)

	def file_delete(self, path, conn):
		if os.path.exists(path):
			os.remove(path)
			self.send_response(CODE_OK, conn)
		else:
			self.send_response(ERR_PATH_NOT_CORRECT, conn)

	def file_info(self, path, conn):
		if os.path.exists(path):
			res = os.stat(path)
			f = open('response.txt', 'w')
			f.write(str(res))
			f.close()
			self.send_file('response.txt', conn)
			os.remove('response.txt')
			self.send_response(CODE_OK, conn)
		else:
			self.send_response(ERR_PATH_NOT_CORRECT, conn)
			return -1

	def file_copy(self, src_path, dest_path, conn):
		if os.path.exists(src_path):
			if not os.path.exists(dest_path):
				if self.check_path_correctness(dest_path):
					shutil.copyfile(src_path, dest_path)
					self.send_response(CODE_OK, conn)
				else:
					self.send_response(ERR_PATH_NOT_CORRECT, conn)
			else:
				self.send_response(ERR_FILE_EXISTS, conn)
		else:
			self.send_response(ERR_PATH_NOT_CORRECT, conn)

	def file_move(self, src_path, dest_path, conn):
		if os.path.exists(src_path):
			if not os.path.exists(dest_path):
				if self.check_path_correctness(dest_path):
					self.file_copy(src_path, dest_path,conn)
					self.file_delete(src_path, conn)
					self.send_response(CODE_OK, conn)
				else:
					self.send_response(ERR_PATH_NOT_CORRECT, conn)
			else:
				self.send_response(ERR_FILE_EXISTS, conn)
		else:
			self.send_response(ERR_PATH_NOT_CORRECT, conn)

	def dir_make(self, path, conn):
		if not os.path.exists(path):
			if self.check_path_correctness(path):
				os.mkdir(path)
				self.send_response(CODE_OK, conn)
			else:
				self.send_response(ERR_PATH_NOT_CORRECT, conn)
		else:
			self.send_response(ERR_DIR_EXISTS, conn)

	def dir_delete(self, path, conn):
		if os.path.exists(path):
			os.rmdir(path)
			self.send_response(CODE_OK, conn)
		else:
			self.send_response(ERR_PATH_NOT_CORRECT, conn)

	def receive_file(self, path, conn):
		if os.path.exists(path):
			self.send_response(ERR_FILE_EXISTS, conn)
		elif self.check_path_correctness(path):
			self.send_response(ERR_PATH_NOT_CORRECT, conn)
		else:
			while True:
				text_file = STORAGE_SERVER_ROOT_PATH + path  # path
				# Receive, output and save file
				with open(text_file, "wb") as fw:
					while True:
						data = conn.recv(BUFFER_SIZE)
						if not data:
							break
						else:
							fw.write(data)
				break
			self.send_response(CODE_OK, conn)

	def send_file(self, path, conn):
		if not os.path.exists(path):
			self.send_response(ERR_PATH_NOT_CORRECT, conn)
		else:
			while True:
				with open(path, 'ab+') as fa:
					l = fa.read(BUFFER_SIZE)
					while l:
						conn.send(l)
						l = fa.read(BUFFER_SIZE)
					fa.close()
				break
			self.send_response(CODE_OK, conn)

	def receive_str(self, conn):
		string = ''
		# Receive, output and save file
		while True:
			data = conn.recv(BUFFER_SIZE)
			if not data:
				break
			else:
				string += data.decode()
		self.send_response(CODE_OK, conn)
		return str

	def establish_connection(self):
		ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ss.bind((socket.gethostname(), STORAGE_SERVER_PORT))
		ss.listen()
		(conn, address) = ss.accept()
		return conn, ss

	def send_response(self, code: int, conn):
		conn.send(code.to_bytes(32, 'big'))

	def check_path_correctness(self, path: str):
		path_list = path.split('/')
		full_path = STORAGE_SERVER_ROOT_PATH + '/'
		for directory in path_list[:len(path) - 2]:
			full_path += directory
			if not os.path.exists(full_path):
				return False
		return True

	def close_connection(self, sock):
		sock.close()

	def init(self, conn):
		if os.path.exists(STORAGE_SERVER_ROOT_PATH):
			shutil.rmtree(STORAGE_SERVER_ROOT_PATH)
			os.mkdir(STORAGE_SERVER_ROOT_PATH)
			self.send_response(CODE_OK, conn)
		else:
			os.mkdir(STORAGE_SERVER_ROOT_PATH)
			self.send_response(CODE_OK, conn)
		self.send_response(shutil.disk_usage(STORAGE_SERVER_ROOT_PATH).free // 2**30, conn)


def ping_from_naming():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(CODE_OK.to_bytes(), (NAMING_SERVER_IP, NAMING_SERVER_PORT))
	sock.close()
