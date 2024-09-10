"""
Assignment 2: Trees for Treemap

=== CSC148 Winter 2024 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Bogdan Simion, David Liu, Diane Horton,
                   Haocheng Hu, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations

import math
import os
from random import randint
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None

        # You will change this in Task 5
        # if len(self._subtrees) > 0:
        #     self._expanded = True
        # else:
        self._expanded = False

        # 1. Initialize self._colour and self.data_size, according to the
        # docstring.
        # 2. Set this tree as the parent for each of its subtrees.
        self.data_size = 0
        num1 = randint(0, 255)
        num2 = randint(0, 255)
        num3 = randint(0, 255)
        self._colour = (num1, num2, num3)

        if subtrees == []:
            self.data_size = data_size
        else:
            for subtree in subtrees:
                subtree._parent_tree = self
                self.data_size += subtree.data_size

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def get_parent(self) -> Optional[TMTree]:
        """Returns the parent of this tree.
        """
        return self._parent_tree

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        # Read the handout carefully to help get started identifying base cases,
        # then write the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # elements of a rectangle, as follows.
        # x, y, width, height = rect
        if self.is_empty() or self.data_size == 0:
            self.rect = (0, 0, 0, 0)
        elif self._subtrees == [] or not self._expanded:
            self.rect = rect
        else:
            self.rect = rect
            self._tm_alg(rect)

    def _tm_alg(self, rect: Tuple[int, int, int, int]) -> None:
        """Helper for update_rectangles.

        """
        x, y, width, height = rect
        used_space = 0
        for i, subtree in enumerate(self._subtrees):
            prop = subtree.data_size / self.data_size
            if width > height:
                sub_width = (width - used_space
                             if i == len(self._subtrees) - 1
                             else int(width * prop))
                new_rect = (x + used_space, y, sub_width, height)
                used_space += sub_width
            else:
                sub_height = (height - used_space
                              if i == len(self._subtrees) - 1
                              else int(height * prop))
                new_rect = (x, y + used_space, width, sub_height)
                used_space += sub_height
            subtree.update_rectangles(new_rect)

    def get_rectangles(self) -> (
            List)[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self.is_empty():
            return []
        elif not self._expanded:
            return [(self.rect, self._colour)]
        else:
            lst = []
            for subtree in self._subtrees:
                lst.extend(subtree.get_rectangles())
            return lst

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two or more rectangles,
        always return the leftmost and topmost rectangle (wherever applicable).
        """
        if self.is_empty() or self.data_size == 0:
            return None
        elif self._subtrees == [] or not self._expanded:
            x, y, w, h = self.rect
            ox, oy = pos[0], pos[1]
            return self if x <= ox <= w + x and y <= oy <= y + h else None
        else:
            for subtree in self._subtrees:
                tree = subtree.get_tree_at_position(pos)
                if tree is not None:
                    return tree
            return None

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if self.is_empty():
            return 0
        elif self._subtrees == []:
            return self.data_size
        else:
            data_size = 0
            for subtree in self._subtrees:
                subtree_size = subtree.update_data_sizes()
                data_size += subtree_size
            self.data_size = data_size
            return data_size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if self.is_empty():
            pass
        elif self._subtrees == [] and (destination._subtrees != []):
            destination._subtrees.append(self)
            self.delete_self()
            self._parent_tree = destination
            root = self._surface()
            root.update_data_sizes()
            root.update_rectangles(root.rect)

    def _surface(self) -> TMTree:
        """Return to the root of the tree.

        """
        root = self
        while root._parent_tree is not None:
            root = root.get_parent()
        return root

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if self._subtrees == [] and not self.is_empty():
            change = math.ceil(self.data_size * abs(factor))
            if factor > 0:
                self.data_size += change
            else:
                self.data_size = max(1, self.data_size - change)

            root = self._surface()
            root.update_data_sizes()
            root.update_rectangles(root.rect)

    def _update_empty_folder(self) -> None:
        """ Update the data_size if a folder is empty.
        """
        parent = self.get_parent()
        if parent is not None and len(parent._subtrees) == 1:
            if parent._subtrees[0].data_size == 0:
                parent.data_size = 0
                parent._update_empty_folder()

    def delete_self(self) -> bool:
        """Removes the current node from the visualization and
        returns whether the deletion was successful.

        Only do this if this node has a parent tree.

        Do not set self._parent_tree to None, because it might be used
        by the visualiser to go back to the parent folder.
        """
        parent = self.get_parent()
        if parent is not None:
            parent._subtrees.remove(self)
            if len(parent._subtrees) == 0:
                parent.data_size = 0
                parent._expanded = False
                parent._update_empty_folder()
                parent.update_rectangles(parent.rect)
            root = self._surface()
            root.update_data_sizes()
            root.update_rectangles(root.rect)
            return True
        return False

    def expand(self) -> None:
        """Expand the folder by one depth.
        If this tree is empty of a leaf, do nothing.
        """
        if self._subtrees == [] or self.is_empty():
            pass
        else:
            self._expanded = True
            self.update_rectangles(self.rect)

    def expand_all(self) -> None:
        """Expand the entire tree from the root.
        """
        self._expand_all_helper()
        self.update_rectangles(self.rect)

    def _expand_all_helper(self) -> None:
        """Helper for expand_all.
        If this tree is empty of a leaf, do nothing.
        """
        if self._subtrees == [] or self.is_empty():
            pass
        else:
            self._expanded = True
            for subtree in self._subtrees:
                subtree._expand_all_helper()

    def collapse(self) -> None:
        """Collapse the folder by one depth.
        If this tree is the root, do nothing
        """
        parent = self.get_parent()
        if parent is not None:
            parent._collapse_helper()
            parent.update_rectangles(parent.rect)

    def _collapse_helper(self) -> None:
        """Helper function for collapse.
        If this tree is empty of a leaf, do nothing.
        """
        if self._subtrees == [] or self.is_empty():
            pass
        else:
            self._expanded = False
            for subtree in self._subtrees:
                subtree._collapse_helper()

    def collapse_all(self) -> None:
        """Collapse the entire tree from the root.
        """
        root = self._surface()
        root._collapse_helper()
        root.update_rectangles(root.rect)

    # Methods for the string representation
    def get_path_string(self) -> str:
        """
        Return a string representing the path containing this tree
        and its ancestors, using the separator for this OS between each
        tree's name.
        """
        if self._parent_tree is None:
            return self._name
        else:
            return self._parent_tree.get_path_string() + \
                self.get_separator() + self._name

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError


class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        if not os.path.isdir(path):
            super().__init__(os.path.basename(path),
                             [], os.path.getsize(path))
        else:
            subtree = []
            for p in os.listdir(path):
                subtree.append(FileSystemTree(os.path.join(path, p)))
            super().__init__(os.path.basename(path), subtree)

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """

        def convert_size(data_size: float, suffix: str = 'B') -> str:
            suffixes = {'B': 'kB', 'kB': 'MB', 'MB': 'GB', 'GB': 'TB'}
            if data_size < 1024 or suffix == 'TB':
                return f'{data_size:.2f}{suffix}'
            return convert_size(data_size / 1024, suffixes[suffix])

        components = []
        if len(self._subtrees) == 0:
            components.append('file')
        else:
            components.append('folder')
            components.append(f'{len(self._subtrees)} items')
        components.append(convert_size(self.data_size))
        return f' ({", ".join(components)})'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
