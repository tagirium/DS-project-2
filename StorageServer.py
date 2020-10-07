import os
import shutil


class StorageServer:
	def file_read(self, path): #?
		pass

	def file_create(self, path):
		file = open(path, 'w+')
		file.close()

	def file_write(self, file, path): #?
		if not os.path.exists(path):
			self.file_move(file, path)

	def file_delete(self, path):
		if os.path.exists(path):
			os.remove(path)

	def file_info(self, path):
		if os.path.exists(path):
			return os.stat(path)

	def file_copy(self, src_path, dest_path):
		shutil.copyfile(src_path, dest_path)

	def file_move(self, src_path, dest_path):
		shutil.copyfile(src_path, dest_path)
		self.file_delete(src_path)

	def dir_open(self, path):
		os.chdir(path)

	def dir_read(self, path):
		if os.path.exists(path):
			entries = os.listdir(path)
			return entries

	def dir_make(self, path):
		if not os.path.exists(path):
			os.mkdir(path)

	def dir_delete(self, path):
		if os.path.exists(path):
			os.rmdir(path)
