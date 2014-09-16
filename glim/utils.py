"""

The utils module is a bunch of functions used inside
the implementation of glim framework.

"""

import shutil
import os
import traceback
import imp

# function performs an import given full path & module


def import_source(module, path, pass_errors=False):
    """

    Function imports a module given full path

    Args
    ----
      module (string): the module name
      path (string): the full path of module
      pass_errors(boolean): the switch for function
        to skip errors or not.

    Returns
    -------
      module (module): the module object.

    Raises
    ------
      e (Exception): any kind of exceptions during importing.

    """
    try:
        m = imp.load_source(module, path)
        return m
    except Exception as e:
        return None

# function performs a parametric import statement, returns None if not found


def import_module(module, pass_errors=False):
    """

    Function imports a module given module name

    Args
    ----
      module (string): the module name
      pass_errors(boolean): the switch for function
        to skip errors or not.

    Returns
    -------
      module (module): the module object.

    Raises
    ------
      exception (Exception): any kind of exceptions during importing.
      import_error(ImportError): import errors during importing.

    Note:
      pass_errors switch will not pass any errors other than ImportError

    """
    frm = module.split('.')
    try:
        m = __import__(module, fromlist=[frm[1]])
        return m
    except ImportError as e:
        if pass_errors:
            return None
        else:
            print(traceback.format_exc())
            return None
    except Exception as e:
        print(traceback.format_exc())
        return None

# function performs a recursive copy of files and folders in the filesystem


def copytree(src, dst, symlinks=False, ignore=None):
    """

    Function recursively copies from directory to directory.

    Args
    ----
      src (string): the full path of source directory
      dst (string): the full path of destination directory
      symlinks (boolean): the switch for tracking symlinks
      ignore (list): the ignore list

    Note:
      After 0.8.4 release, if the source directory doesn't exist,
      it will create the directory given full path.

    """
    if not os.path.exists(dst):
        os.mkdir(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
