from __future__ import annotations
from typing import Optional
import yaml
# -------------------------------------------

from typing import TypeVar
TreeNodeType = TypeVar('TreeNodeType', bound='TreeNode')

class TreeNode:
    def __init__(self, name : str, parent : Optional[TreeNodeType] = None):
        self._name : str = name
        self._parent : TreeNodeType = parent
        self._children : Optional[list[TreeNodeType]] = None

    def _add_child(self, node : TreeNodeType):
        if node.get_parent() != self:
            raise ValueError(f'Node already has parent')
        self._children.append(node)

    def get_name(self) -> str:
        return self._name

    # -------------------------------------------
    # descendants

    def get_subnodes(self) -> list[TreeNodeType]:
        subnodes = []
        for child in self.get_child_nodes():
            subnodes.append(child)
            subnodes += child.get_subnodes()
        return subnodes

    def get_child_nodes(self) -> list[TreeNodeType]:
        return self._children

    def get_yaml_tree(self, skip_empty: bool = True) -> str:
        the_yaml = yaml.dump(data=self.get_dict(), indent=4)
        if skip_empty:
            the_yaml = the_yaml.replace(f': {{}}', '')
        return the_yaml

    def get_dict(self) -> Optional[dict]:
        the_dict = {self._name: {}}
        for child in self.get_child_nodes():
            the_dict[self._name].update(child.get_dict())
        return the_dict

    # -------------------------------------------
    # ancestors

    def get_ancestors(self) -> list[TreeNodeType]:
        current = self
        ancestors = []
        while current._parent:
            ancestors.append(current._parent)
            current = current._parent
        return ancestors

    def get_parent(self) -> Optional[TreeNodeType]:
        return self._parent

    def get_root(self) -> TreeNodeType:
        current = self
        while current.get_parent():
            current = current.get_parent()
        return current
