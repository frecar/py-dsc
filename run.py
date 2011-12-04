import os
import sys

settings_folder= sys.argv[0]
settings_file = sys.argv[1]


def get_list_of_already_unrared_files():
    rar_files = []
    try:
        f = open("myfile.txt", 'r')
        for line in f:
            if len(str(line)) and line != "\n":
                rar_files.append(line)
        f.close()
        return rar_files
    except Exception:
        return []

def add_file_to_unrar_list(filename):
    rar_files = get_list_of_already_unrared_files()
    rar_files.append(filename)
    f = open("myfile.txt", "w")

    for filename in rar_files:
        if len(str(filename).strip()):
            f.write(filename)
    
    f.close()

def filename_in_unrared_files(filename):
    try:
        f = open("myfile.txt", "r")
        result = filename in f.read()
        f.close()
        return result
    except Exception:
        return False

def find_rar_files(folder):
    rar_files = []
    unrared_files = get_list_of_already_unrared_files()

    for root, dirs, files in os.walk(folder, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            if '.rar' in filename:
                if not filename_in_unrared_files(filename):
                    rar_files.append(filename)
                    add_file_to_unrar_list(filename)

    return rar_files

#for f in find_rar_files("/Volumes/Data/tvshows"):
#   os.system("open " + f)


