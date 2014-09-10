import shutil
import os
import traceback
import imp

# function performs an import given full path & module
def import_source(module, path, pass_errors = False):
    try:
        m = imp.load_source(module, path)
        return m
    except Exception, e:
        return None

# function performs a parametric import statement, returns None if not found
def import_module(module, pass_errors = False):

    frm = module.split('.')
    try:
        m = __import__(module, fromlist = [frm[1]])
        return m
    except ImportError, e:
        if pass_errors:
            return None
        else:
            print traceback.format_exc()
            return None
    except Exception, e:
        print traceback.format_exc()
        return None

# function performs a recursive copy of files and folders in the filesystem
def copytree(src, dst, symlinks = False, ignore = None):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)