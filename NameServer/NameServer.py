import socket

class Directory(object):

    def __init__(self, name):
        self.list = []
        self.name = name

    def add_child(self, obj):
        obj.prev = self
        self.list.append(obj)

    def print_children(self):
        for i in range(len(self.list)):
            print('/ ', self.list[i].name)

    def find_by_name(self, name):
        if name == '/':
            return self
        for i in range(len(self.list)):
            if self.list[i].name == name:
                return  self.list[i]
        return None

    def add_file_to_path(self, path):
        dirs = []
        dirs = path.split('/')
        dirs[0] = '/'
        name = dirs[len(dirs)-1]
        dirs.pop()
        depth = len(dirs)-1
        dir = self
        if depth == 0:
            dir.add_child(File(name))
            return
        for i in range(depth):
            dir = dir.find_by_name(dirs[i+1])
        dir.add_child(File(name))

    def add_directory_to_path(self, path):
        dirs = []
        dirs = path.split('/')
        dirs[0] = '/'
        name = dirs[len(dirs)-1]
        dirs.pop()
        depth = len(dirs)-1
        dir = self
        if depth == 0:
            dir.add_child(Directory(name))
            return
        for i in range(depth):
            dir = dir.find_by_name(dirs[i+1])
        dir.add_child(Directory(name))

    def remove_from_path(self, path):
        dirs = []
        dirs = path.split('/')
        dirs[0] = '/'
        name = dirs[len(dirs) - 1]
        dirs.pop()
        depth = len(dirs)-1
        dir = self

        if depth == 0:
            for i in range(len(dir.list)):
                if dir.list[i].name == name:
                    dir.list.pop(i)
                    print('deleted')
                    return 0
                else:
                    print('not this one')
        for i in range(depth):
            dir = dir.find_by_name(dirs[i+1])

        for i in range(len(dir.list)):
            if dir.list[i].name == name:
                dir.list.pop(i)
                #print('deleted')
                return 0
            #else:
                #print('not this one')
        return 1

    def get_from_path(self, path):
        path = path + '/'
        dirs = []
        dirs = path.split('/')
        dirs[0] = '/'
        name = dirs[len(dirs) - 1]
        dirs.pop()
        depth = len(dirs) - 1
        dir = self
        print(dirs)
        if depth == 0:
            return dir
        for i in range(depth):
            dir = dir.find_by_name(dirs[i + 1])
        return dir

    def go_to_root(self):
        dir = self
        while(dir.name != '/'):
            dir = self.prev
        return dir


class File(object):

    def __init__(self, name):
        self.name = name

def initialize():
    directory_tree = Directory('/')
    return directory_tree

def file_create(root:Directory,path):
    root.add_file_to_path(path)
    return

def file_read():
    return

def file_write():
    return

def file_delete():
    return

def file_info():
    return

def file_copy():
    return

def file_move():
    return

def open_directory():
    return

def read_directory():
    return

def make_directory():
    return

def delete_directory():
    return


"""
command =  '/lolkek/cheburek/a.txt'
command2 = '/lolkek/pisos'
command2 = '/lolkek/pisos'

directory_tree = Directory('/')
directory_tree.add_child(Directory('lolkek'))
directory_tree.list[0].add_child(Directory('cheburek'))
directory_tree.add_child(Directory('keklol'))
directory_tree.add_child(Directory('arbidol'))

directory_tree.add_file_to_path(command)
directory_tree.add_directory_to_path(command2)
#directory_tree.remove_from_path(command)

directory_tree = directory_tree.get_from_path('/lolkek')

directory_tree = directory_tree.go_to_root()
directory_tree.print_children()
print(directory_tree.name)

#directory_tree.find_by_name('lolkek').print_children()
#directory_tree.print_children()"""

def resolve(str):

    arr = [None, None, None, None]
    arr2 = str.split('||')
    for i in range(4):
        if i < len(arr2)-1:
            arr[i] = arr2[i]
    return arr

work_dir = None
str_from_client = 'initialize||'
i = 0
while i<2:
    #TODO wait for client request
    #TODO resolve request

    from_client = resolve(str_from_client)

    print(from_client)
    if from_client[0] == 'initialize':
        work_dir = initialize()
        print('initialized')
    elif from_client[0] == 'file_create':
        file_create(work_dir, from_client[1])
        work_dir.print_children()
        print('file created')
    elif from_client[0] == 'file_read':
        print('done')
    elif from_client[0] == 'file_write':
        print('done')
    elif from_client[0] == 'file_delete':
        print('done')
    elif from_client[0] == 'file_info':
        print('done')
    elif from_client[0] == 'file_copy':
        print('done')
    elif from_client[0] == 'file_move':
        print('done')
    elif from_client[0] == 'open_directory':
        print('done')
    elif from_client[0] == 'read_directory':
        print('done')
    elif from_client[0] == 'make_directory':
        print('done')
    elif from_client[0] == 'delete_directory':
        print('done')

    str_from_client = 'file_create||/a.txt||'
    #TODO Do operations on dir tree
    #TODO Send instructions and files to storage servers
    i += 1





