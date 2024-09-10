import os

from hypothesis import given
from hypothesis.strategies import integers

from tm_trees import TMTree, FileSystemTree

# This should be the path to the "workshop" folder in the sample data.
# You may need to modify this, depending on where you downloaded and
# extracted the files.

EXAMPLE_PATH = os.path.join(os.getcwd(), 'example-directory', 'workshop')


def test_parent_tree_attributes_empty() -> None:
    """Test TMTree attributes are being correctly set.
    """
    t1 = TMTree(None, [], 0)
    assert t1.data_size == 0
    assert t1._parent_tree is None
    assert True


def test_parent_tree_attributes_variety_depth() -> None:
    """Test TMTree attributes are being correctly set for depth 1, 2, 3 , 4, 5
    """
    tmt1a = TMTree('a', [], 10)
    tmt1b = TMTree('b', [], 15)
    tmt1c = TMTree('c', [], 20)
    tmt2a = TMTree('a', [tmt1a])
    tmt2b = TMTree('b', [tmt1b, tmt1a, tmt1c])
    tmt3a = TMTree('a', [tmt2b])
    tmt3b = TMTree('b', [tmt2b, tmt2a, tmt1c])
    tmt4a = TMTree('a', [tmt3b])
    tmt4b = TMTree('b', [tmt3b, tmt3a, tmt1c])
    tmt5 = TMTree('c', [tmt4b, tmt3a, tmt1a])
    temp = TMTree('x', [tmt4a])
    trees = [tmt1a, tmt1b, tmt1c, tmt2a,
             tmt2b, tmt3a, tmt3b, tmt4a, tmt4b, tmt5]

    # Test colour set correctly
    for tree in trees:
        colour = tree._colour
        assert isinstance(colour, tuple)
        assert len(colour) == 3
        assert is_valid_colour(colour)

    # Test data size
    answer = [10, 15, 20, 10, 45, 45, 75, 75, 140, 195]
    for i in range(len(trees)):
        assert trees[i].data_size == answer[i]

    # Test parent
    for i in range(len(trees) - 1):
        assert trees[i].get_parent() is not None
    assert tmt4b.get_parent() is tmt5
    assert tmt2a.get_parent() is tmt3b
    assert tmt5.get_parent() is None


def test_single_file() -> None:
    """Test a tree with a single file.
    """
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, 'draft.pptx'))
    assert tree._name == 'draft.pptx'
    assert tree._subtrees == []
    assert tree._parent_tree is None
    assert tree.data_size == 58
    assert is_valid_colour(tree._colour)


def test_file_tree_attributes_depth_two() -> None:
    """Test FileSystemTree attributes are being correctly set for
    depth 2.
    """
    temp = os.path.join(EXAMPLE_PATH, "activities")
    p2 = os.path.join(temp, "images")
    tree = FileSystemTree(p2)

    assert tree._name == 'images'
    assert tree._parent_tree is None
    assert tree.data_size == 69
    assert is_valid_colour(tree._colour)
    assert len(tree._subtrees) == 2
    for subtree in tree._subtrees:
        assert subtree._parent_tree is tree

    assert len(tree._subtrees) == 2
    subtree1 = tree._subtrees[0]
    assert subtree1._name == 'Q3.pdf' or subtree1._name == 'Q2.pdf'
    assert subtree1._subtrees == []
    assert subtree1.data_size == 49 or subtree1.data_size == 20
    assert is_valid_colour(subtree1._colour)
    assert isinstance(subtree1._colour, tuple)

    subtree2 = tree._subtrees[1]
    assert subtree2._name == 'Q2.pdf' or subtree2._name == 'Q3.pdf'
    assert subtree2._subtrees == []
    assert subtree2.data_size == 20 or subtree2.data_size == 49
    assert is_valid_colour(subtree2._colour)
    assert isinstance(subtree2._colour, tuple)


def test_file_tree_attributes_depth_three() -> None:
    """Test FileSystemTree attributes are being correctly set for depth 3.
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    assert tree._name == 'workshop'
    assert tree._parent_tree is None
    assert tree.data_size == 151
    assert is_valid_colour(tree._colour)

    assert len(tree._subtrees) == 3
    for subtree in tree._subtrees:
        assert subtree.get_parent() is tree


def test_example_data() -> None:
    """Test the root of the tree at the 'workshop' folder in the example data
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    assert tree._name == 'workshop'
    assert tree._parent_tree is None
    assert tree.data_size == 151
    assert is_valid_colour(tree._colour)

    assert len(tree._subtrees) == 3
    for subtree in tree._subtrees:
        # Note the use of is rather than ==.
        # This checks ids rather than values.
        assert subtree._parent_tree is tree


def test_task2() -> None:
    """Test updating and getting rectangles on standard tree.
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.update_rectangles((0, 0, 200, 100))
    tree.expand_all()
    rects = tree.get_rectangles()
    assert len(rects) == 6


@given(integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000))
def test_single_file_rectangles(x, y, width, height) -> None:
    """Test that the correct rectangle is produced for a single file."""
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, 'draft.pptx'))
    tree.update_rectangles((x, y, width, height))
    rects = tree.get_rectangles()

    # This should be just a single rectangle and colour returned.
    assert len(rects) == 1
    rect, colour = rects[0]
    assert rect == (x, y, width, height)
    assert is_valid_colour(colour)


@given(integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000),
       integers(min_value=100, max_value=1000))
def test_single_file_rectangles(x, y, width, height) -> None:
    """Test that the correct rectangle is produced for a single file."""
    tree = FileSystemTree(os.path.join(EXAMPLE_PATH, 'draft.pptx'))
    tree.update_rectangles((x, y, width, height))
    rects = tree.get_rectangles()

    # This should be just a single rectangle and colour returned.
    assert len(rects) == 1
    rect, colour = rects[0]
    assert rect == (x, y, width, height)
    assert is_valid_colour(colour)


def test_example_data_rectangles() -> None:
    """This test sorts the subtrees, because different operating systems have
    different behaviours with os.listdir.

    You should *NOT* do any sorting in your own code
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    _sort_subtrees(tree)

    tree.update_rectangles((0, 0, 200, 100))
    rects = tree.get_rectangles()

    # IMPORTANT: This test should pass when you have completed Task 2, but
    # will fail once you have completed Task 5.
    # You should edit it as you make progress through the tasks,
    # and add further tests for the later task functionality.
    assert len(rects) == 1


def test_change_size_ascendant() -> None:
    # See how changing size affects the other subtrees data size and rect
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.update_rectangles((0, 0, 200, 100))
    _sort_subtrees(tree)

    assert tree.data_size == 151
    leaf = tree._subtrees[0]._subtrees[1]._subtrees[0]
    x, y, z, w = leaf.rect
    assert leaf.data_size == 20
    assert leaf._name == 'Q2.pdf'

    leaf.change_size(0.1)
    assert leaf.rect == (x, y, z, w)
    assert leaf.data_size == 22
    assert leaf.get_parent().data_size == 71


def test_delete_self() -> None:
    """See if deleting leafs, nodes, root, empty folders would change the
    other node's data size, and rect
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.update_rectangles((0, 0, 200, 100))
    _sort_subtrees(tree)
    example_node = tree._subtrees[1]
    assert example_node._name == 'draft.pptx'
    x, y, z, w = example_node.rect

    assert tree.data_size == 151
    leaf = tree._subtrees[0]._subtrees[1]._subtrees[0]
    other_leaf = tree._subtrees[0]._subtrees[1]._subtrees[1]
    assert leaf.data_size == 20
    assert leaf._name == 'Q2.pdf'

    # delete folder
    folder = tree._subtrees[len(tree._subtrees) - 1]
    assert folder.delete_self()
    assert len(folder.get_parent()._subtrees) == 2

    # rect and data_size changed
    assert tree.data_size != 151
    assert len(tree._subtrees) == 2
    assert example_node._name == 'draft.pptx'
    assert example_node.rect == (x, y, z, w)

    # deleting leaf
    assert leaf.delete_self()
    assert other_leaf.delete_self()
    parent = leaf.get_parent()
    assert len(parent._subtrees) == 0

    # delete empty folder
    ans = parent.delete_self()
    assert ans
    ggp = parent.get_parent()
    assert len(ggp._subtrees) == 1

    # delete root
    gggp = ggp.get_parent()
    assert not gggp.delete_self()


def test_delete_folders_with_no_files() -> None:
    """Test whether deleting a single file resulting in chained empty folders
    causes folders to be deleted and what happens in these situations
    """
    tree = FileSystemTree(EXAMPLE_PATH)
    tree.update_rectangles((0, 0, 200, 100))
    tree.update_data_sizes()
    _sort_subtrees(tree)
    tree._subtrees[0]._subtrees[0].delete_self()
    tree._subtrees[0]._subtrees[0]._subtrees[0].delete_self()
    tree._subtrees[0]._subtrees[0]._subtrees[0].delete_self()

    # We have a folder in a folder, both do not contain files
    new_leaf = tree._subtrees[0]._subtrees[0]
    new_leaf.delete_self()
    assert new_leaf.get_parent()._name == 'activities'
    assert len(new_leaf.get_parent()._subtrees) == 0
    assert new_leaf.get_parent().data_size == 0


##############################################################################
# Helpers
##############################################################################
def is_valid_colour(colour: tuple[int, int, int]) -> bool:
    """Return True iff <colour> is a valid colour. That is, if all of its
    values are between 0 and 255, inclusive.
    """
    for i in range(3):
        if not 0 <= colour[i] <= 255:
            return False
    return True


def _sort_subtrees(tree: TMTree) -> None:
    """Sort the subtrees of <tree> in alphabetical order.
    THIS IS FOR THE PURPOSES OF THE SAMPLE TEST ONLY; YOU SHOULD NOT SORT
    YOUR SUBTREES IN THIS WAY. This allows the sample test to run on different
    operating systems.

    This is recursive, and affects all levels of the tree.
    """
    if not tree.is_empty():
        for subtree in tree._subtrees:
            _sort_subtrees(subtree)

        tree._subtrees.sort(key=lambda t: t._name)


if __name__ == '__main__':
    import pytest

    pytest.main(['a2_sample_test.py'])
