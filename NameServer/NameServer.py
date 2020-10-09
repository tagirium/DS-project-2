import socket

class Directory(object):
    list = []

    def __init__(self, name):
        self.list = []
        self.name = name

    def add_child(self, obj):
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
                    return
                else:
                    print('not this one')
        for i in range(depth):
            dir = dir.find_by_name(dirs[i+1])

        for i in range(len(dir.list)):
            if dir.list[i].name == name:
                dir.list.pop(i)
                print('deleted')
                return
            else:
                print('not this one')
        



class File(object):

    def __init__(self, name):
        self.name = name

command =  '/a.txt'
command2 = '/lolkek/pisos'

directory_tree = Directory('/')
directory_tree.add_child(Directory('lolkek'))
directory_tree.add_child(Directory('cheburek'))
directory_tree.add_child(Directory('keklol'))
directory_tree.add_child(Directory('arbidol'))
directory_tree.add_file_to_path(command)
directory_tree.add_directory_to_path(command2)
directory_tree.remove_from_path(command)
directory_tree.find_by_name('lolkek').print_children()
directory_tree.print_children()






