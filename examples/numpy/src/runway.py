import pathlib
import tempfile
import zipfile
import os
import sys
import robot


zipapplocation = pathlib.Path(sys.path[0])

if zipapplocation.suffix in {".pyz", ".exe"}:
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
