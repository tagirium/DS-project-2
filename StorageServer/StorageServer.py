import shutil
import os
from StorageServer.codes import *
import socket


class StorageServer:

	def __init__(self, port):
		self.NAMING_SERVER_PORT = port

	def file_read(self, path):
		if os.path.exists(path):
			self.send_file(path)
		else:
			self.error_response(ERR_PATH_NOT_CORRECT)

	def file_create(self, path):
		if self.check_path_correctness(path):
			if not os.path.exists(path):
				file = open(path, 'w+')
				file.close()
			else:
				self.error_response(ERR_FILE_EXISTS)
		else:
			self.error_response(ERR_PATH_NOT_CORRECT)

	def file_write(self, path):
		if not os.path.exists(path):
			if self.check_path_correctness(path):
				self.receive_file(path)
			else:
				self.error_response(ERR_PATH_NOT_CORRECT)
		else:
			self.error_response(ERR_FILE_EXISTS)

	def file_delete(self, path):
		if os.path.exists(path):
			os.remove(path)
		else:
			self.error_response(ERR_PATH_NOT_CORRECT)

	def file_info(self, path):
		if os.path.exists(path):
			return os.stat(path)
		else:
			self.error_response(ERR_PATH_NOT_CORRECT)
			return -1

	def file_copy(self, src_path, dest_path):
		if os.path.exists(src_path):
			if not os.path.exists(dest_path):
				if self.check_path_correctness(dest_path):
					shutil.copyfile(src_path, dest_path)
				else:
					self.error_response(ERR_PATH_NOT_CORRECT)
			else:
				self.error_response(ERR_FILE_EXISTS)
		else:
			self.error_response(ERR_PATH_NOT_CORRECT)

	def file_move(self, src_path, dest_path):
		if os.path.exists(src_path):
			if not os.path.exists(dest_path):
				if self.check_path_correctness(dest_path):
					self.file_copy(src_path, dest_path)
					self.file_delete(src_path)
				else:
					self.error_response(ERR_PATH_NOT_CORRECT)
			else:
				self.error_response(ERR_FILE_EXISTS)
		else:
			self.error_response(ERR_PATH_NOT_CORRECT)

	def dir_open(self, path):
		if os.path.exists(path):
			os.chdir(path)
		else:
			self.error_response(ERR_PATH_NOT_CORRECT)

	def dir_read(self, path):
		if os.path.exists(path) and os.path.isdir(path):
			entries = os.listdir(path)
			return ', '.join(list(map(str, entries)))
		else:
			self.error_response(ERR_PATH_NOT_CORRECT)

	def dir_make(self, path):
		if not os.path.exists(path):
			if self.check_path_correctness(path):
				os.mkdir(path)
			else:
				self.error_response(ERR_PATH_NOT_CORRECT)
		else:
			self.error_response(ERR_DIR_EXISTS)

	def dir_delete(self, path):
		if os.path.exists(path):
			os.rmdir(path)
		else:
			self.error_response(ERR_PATH_NOT_CORRECT)

	def ping_from_naming(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((socket.gethostname(), self.NAMING_SERVER_PORT))
		sock.send(CODE_OK.to_bytes())

	def receive_file(self, path):
		if os.path.exists(path):
			self.error_response(ERR_FILE_EXISTS)
		elif self.check_path_correctness(path):
			self.error_response(ERR_PATH_NOT_CORRECT)
		else:
			ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ss.bind((socket.gethostname(), STORAGE_SERVER_PORT))
			ss.listen()
			while True:
				(conn, address) = ss.accept()
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
			ss.close()

	def send_file(self, path):
		if not os.path.exists(path):
			self.error_response(ERR_PATH_NOT_CORRECT)
		else:
			ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			ss.bind((socket.gethostname(), STORAGE_SERVER_PORT))
			ss.listen()
			while True:
				(conn, address) = ss.accept()
				with open(path, 'ab+') as fa:
					l = fa.read(BUFFER_SIZE)
					while l:
						conn.send(l)
						l = fa.read(BUFFER_SIZE)
					fa.close()
				break
			ss.close()

	def receive_str(self):
		ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ss.bind((socket.gethostname(), STORAGE_SERVER_PORT))
		ss.listen()
		string = ''
		while True:
			(conn, address) = ss.accept()
			# Receive, output and save file
			while True:
				data = conn.recv(BUFFER_SIZE)
				if not data:
					break
				else:
					string += data.decode()
			if not address:
				break
		ss.close()
		return str

	def error_response(self, code: int):
		ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ss.bind((socket.gethostname(), STORAGE_SERVER_PORT))
		ss.listen()
		while True:
			(conn, address) = ss.accept()
			conn.send(code.to_bytes(32, 'big'))
			if not address:
				break
		ss.close()

	def check_path_correctness(self, path: str):
		path_list = path.split('/')
		full_path = STORAGE_SERVER_ROOT_PATH + '/'
		for directory in path_list[:len(path) - 2]:
			full_path += directory
			if not os.path.exists(full_path):
				return False
		return True
