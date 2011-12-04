import os, sys, time, platform, ctypes, shutil
from stat import *
from heapq import *

settings_folder = sys.argv[0]
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


def free_space(folder):
    # Return folder/drive free space (in bytes)
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        folder_stat = os.statvfs(folder)
        return (folder_stat.f_bavail * folder_stat.f_frsize)


def walk_flat_file(top, callback):
    for f in os.listdir(top):
        callback(os.path.join(top, f))


def visitfile(file):
    print '%s created: %s' % (file, creation_time(file))


def creation_time(path):
    return os.stat(path)[ST_CTIME]


def build_heap(root_path):
    heap = []
    for f in os.listdir(root_path):
        path = os.path.join(root_path, f)
        heappush(heap, (creation_time(path), path))
    return heap


def is_directory(path):
    return S_ISDIR(os.stat(path)[ST_MODE])


def delete_thing(path):
    if is_directory(path):
        shutil.rmtree(path)
    else:
        os.remove(path)


def enough_free_space(root_path, required_bytes):
    return free_space(root_path) >= required_bytes


def main(media_path, required_bytes):
    if not enough_free_space(media_path, required_bytes):
        print "ja"
        heap = build_heap(media_path)
        while not enough_free_space(media_path, required_bytes) and len(heap) > 0:
            print "deleting " + str(heap[0][1]) + " with " + str(free_space(media_path)) + " bytes of free space."
            delete_thing(heappop(heap)[1])

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
    if enough_free_space(sys.argv[1], int(sys.argv[2])):
        print "finished with enough free space"
    else:
        print "didnt free up as much as desired"