import shutil
import os

# function performs a parametric import statement, returns None if not found
def import_module(module, frm):
    try:
        m = __import__(module, fromlist = [frm])
        return m
    except Exception, e:
        return None

# function performs a recursive copy of files and folders in the filesystem
def copytree(src, dst, symlinks = False, ignore = None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)