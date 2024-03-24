from __future__ import annotations
from typing import Optional
# -------------------------------------------

class TreeNode:
    def __init__(self, name : str, parent : Optional[TreeNode] = None):
        self._name : str = name
        self._parent : TreeNode = parent
        self._children : Optional[list] = None

    def _add_child(self, node : TreeNode):
        if node.get_parent() != self:
            raise ValueError(f'Node already has parent')
        if self._children is None:
            self._children = []
        self._children.append(node)

    def get_name(self) -> str:
        return self._name

    # -------------------------------------------
    # descendants

    def get_subnodes(self) -> list[TreeNode]:
        subnodes = []
        for child in self.get_child_nodes():
            subnodes.append(child)
            subnodes += child.get_subnodes()
        return subnodes

    def get_child_nodes(self) -> list[TreeNode]:
        return self._children

    def get_tree(self, max_child_size : int = 100) -> str:
        sub_dict = self.get_dict()[self._name]
        for key, value in [(key,value) for (key, value) in sub_dict.items() if isinstance(value, dict)]:
            elem_count = get_total_elements(recursive_dict=value)
            if elem_count > max_child_size:
                sub_dict[key] = f': {key} exceeds limit of {max_child_size} elements contains {elem_count} files/folders'

        tree = get_pretty_tree(the_dict={self._name : sub_dict})
        tree = tree.replace('{}', '')
        return tree

    def get_dict(self) -> Optional[dict]:
        the_dict = {self._name: {}}
        for child in self.get_child_nodes():
            the_dict[self._name].update(child.get_dict())
        return the_dict

    # -------------------------------------------
    # ancestors

    def get_ancestors(self) -> list[TreeNode]:
        current = self
        ancestors = []
        while current._parent:
            ancestors.append(current._parent)
            current = current._parent
        return ancestors

    def get_parent(self) -> Optional[TreeNode]:
        return self._parent

    def get_root(self) -> TreeNode:
        current = self
        while current.get_parent():
            current = current.get_parent()
        return current


def get_pretty_tree(the_dict, prefix='', is_last=True) -> str:
    output = ''
    for index, (key, value) in enumerate(the_dict.items()):
        connector = '└── ' if is_last else '├── '
        new_prefix = prefix + ('    ' if is_last else '│   ')

        if isinstance(value, dict) and value:
            output = f'{prefix}{connector}{key}\n'
            last_child = len(value) - 1
            for sub_index, (sub_key, sub_value) in enumerate(value.items()):
                sub_is_last = sub_index == last_child
                output += get_pretty_tree({sub_key: sub_value}, new_prefix, sub_is_last)
        else:
            output += f'{prefix}{connector}{key} {value}\n'
    return output


def get_total_elements(recursive_dict: dict) -> int:
    count = 0
    for key, value in recursive_dict.items():
        count += 1
        if isinstance(value, dict):
            count += get_total_elements(value)
    return count
