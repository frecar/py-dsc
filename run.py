import os, sys, time, platform, ctypes, shutil
from stat import *
from heapq import *







def free_space(folder):
    """ Return folder/drive free space (in bytes)
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        return os.statvfs(folder).f_bfree

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
			print "deleting " + heap[0][1] + " with " + free_space(root_path) + " bytes of free space."
			delete_thing(heappop(heap)[1])
	
if __name__ == '__main__':
	main(sys.argv[1], int(sys.argv[2]))
	if enough_free_space(sys.argv[1], int(sys.argv[2])):
		print "finished with enough free space"
	else:
		print "didnt free up as much as desired"
