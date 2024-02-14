from __future__ import annotations
from typing import Optional
from pathlib import Path
import os

# -------------------------------------------


class FsysNode:
    def __init__(self, path : str):
        self.path : str = path
        self.name : str = os.path.basename(path)
        self._subnodes : Optional[list[FsysNode]] = None

    def select_file_subnodes(self, allowed_formats : list[str]) -> list[FsysNode]:
        selected_node = []
        file_nodes  = self.get_file_subnodes()
        for node in file_nodes:
            suffix = node.get_suffix()
            if suffix in allowed_formats:
                selected_node.append(node)

        return selected_node

    def get_file_subnodes(self) -> list[FsysNode]:
        return [des for des in self.get_subnodes() if des.get_is_file()]

    def get_subnodes(self):
        if self._subnodes is None:
            path_list = list(Path(self.path).rglob('*'))
            self._subnodes: list[FsysNode] = [FsysNode(str(path)) for path in path_list]
        return self._subnodes

    def get_suffix(self) -> Optional[str]:
        try:
            suffix = self.name.split('.')[-1]
        except:
            suffix = None
        return suffix

    def get_epochtime_last_modified(self) -> float:
        return os.path.getmtime(self.path)

    def get_size_in_MB(self) -> float:
        return os.path.getsize(self.path) / (1024 * 1024)

    def get_is_resources(self) -> bool:
        return self.get_is_dir() or self.get_is_file()

    def get_is_file(self) -> bool:
        return os.path.isfile(self.path)

    def get_is_dir(self) -> bool:
        return os.path.isdir(self.path)



if __name__ == "__main__":
    home_node = FsysNode(path='/home/daniel/OneDrive/Downloads/')
    # print(home_node.get_file_nodes())
    # for node in home_node.select_file_nodes(allowed_formats=['png']):
    #     print(node.name)