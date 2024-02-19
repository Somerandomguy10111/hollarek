from __future__ import annotations
from typing import Optional
from pathlib import Path
import os
import tempfile, shutil
# -------------------------------------------

class FsysNode:
    def __init__(self, path : str):
        self._path : str = path
        self._subnodes : Optional[list[FsysNode]] = None
        if not (self.is_dir() or self.is_file()):
            raise FileNotFoundError(f'Path {path} is not a file/folder')

    # -------------------------------------------
    # sub

    def select_file_subnodes(self, allowed_formats : list[str]) -> list[FsysNode]:
        selected_node = []
        file_nodes  = self.get_file_subnodes()
        for node in file_nodes:
            suffix = node.get_suffix()
            if suffix in allowed_formats:
                selected_node.append(node)

        return selected_node


    def get_file_subnodes(self) -> list[FsysNode]:
        return [des for des in self.get_subnodes() if des.is_file()]


    def get_subnodes(self) -> list[FsysNode]:
        if self._subnodes is None:
            path_list = list(Path(self._path).rglob('*'))
            self._subnodes: list[FsysNode] = [FsysNode(str(path)) for path in path_list]
        return self._subnodes

    # -------------------------------------------
    # get

    def get_zip(self) -> bytes:
        with tempfile.TemporaryDirectory() as write_dir:
            zip_basepath = os.path.join(write_dir,'zipfile')
            if self.is_dir():
                shutil.make_archive(base_name=zip_basepath, format='zip', root_dir=self.get_path())
            else:
                containing_dir_path = os.path.join(write_dir, 'dir')
                os.makedirs(containing_dir_path, exist_ok=True)
                shutil.copy(src=self.get_path(), dst=os.path.join(containing_dir_path, self.get_name()))
                shutil.make_archive(base_name=zip_basepath, format='zip', root_dir=containing_dir_path)

            with open(f'{zip_basepath}.zip', 'rb') as file:
                zip_bytes = file.read()

        return zip_bytes

    # -------------------------------------------
    # resource info

    def get_path(self) -> str:
        return self._path

    def get_name(self) -> str:
        return os.path.basename(self._path)

    def get_suffix(self) -> Optional[str]:
        try:
            suffix = self.get_name().split('.')[-1]
        except:
            suffix = None
        return suffix

    def get_epochtime_last_modified(self) -> float:
        return os.path.getmtime(self._path)

    def get_size_in_MB(self) -> float:
        return os.path.getsize(self._path) / (1024 * 1024)

    def is_file(self) -> bool:
        return os.path.isfile(self._path)

    def is_dir(self) -> bool:
        return os.path.isdir(self._path)






if __name__ == "__main__":
    test_path = '/home/daniel/OneDrive/Downloads/test'
    print(os.path.isfile(test_path))
    test_node = FsysNode(path=test_path)
    test_zip_bytes  = test_node.get_zip()


    with open('test.zip', 'wb') as the_file:
        the_file.write(test_zip_bytes)

    # print(home_node.get_file_nodes())
    # for node in home_node.select_file_nodes(allowed_formats=['png']):
    #     print(node.name)
