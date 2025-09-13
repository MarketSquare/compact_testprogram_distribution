import pathlib
import tempfile
import zipfile
import os
import sys
import robot
import zipimport


# This is to improve the speed in python versions 3.10 and 3.11
# see hhttps://github.com/python/cpython/issues/103200
#
# while this does work in this example, it might have side effects
# in other applications. Use with caution.
#
# according to the robotframework maintainer this
# will lead to bugs in robotframework (which happen to
# not be relevant for this example)
zipimport.zipimporter.invalidate_caches = lambda _: None


zipapplocation = pathlib.Path(sys.path[0])

if zipapplocation.suffix in {".pyz", ".exe"}:
    # This is a wild hack which uses temporary directory to make numpy work
    # in a zipapp. It extracts all files which are in the same top level directory
    # as a .pyd, .so or .dll file into a temporary directory and adds this
    # directory to sys.path. This way the dynamic libraries can be found by
    # numpy.
    #
    # This is a hack and might break in the future or has other side effects.
    #
    # This is for educational purposes only. Do not use this unless you thouroughly
    # understand the implications.

    dir_tobuildup_dependencies_path = pathlib.Path(tempfile.mkdtemp())

    with zipfile.ZipFile(zipapplocation, "r") as z:
        pathsOfFilesInzipapp = (pathlib.Path(item.filename) for item in z.filelist)
        interesting_trees = {item.parts[0] for item in pathsOfFilesInzipapp if item.suffix in {".pyd", ".so", ".dll"}}
        files_in_zip = (item for item in z.filelist if not item.is_dir())
        interesting_files_in_zip = list(item for item in files_in_zip if pathlib.Path(item.filename).parts[0] in interesting_trees)

        for item in interesting_files_in_zip:
            z.extract(item, path=dir_tobuildup_dependencies_path)

    numpy_extra_path = dir_tobuildup_dependencies_path / "numpy/.libs"
    if numpy_extra_path.exists():
        os.add_dll_directory(numpy_extra_path)

    sys.path.insert(0, str(dir_tobuildup_dependencies_path))

def main():
    robot.run_cli()
