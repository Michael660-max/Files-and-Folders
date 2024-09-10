from papers import PaperTree


def test_parent_tree_attributes_empty() -> None:
    """Test if all methods in TMTree can be called without error on Paper.
    """
    paper_tree = PaperTree('CS1', [], all_papers=True, by_year=True)
    paper_tree.update_rectangles((0, 0, 1200, 670))
    assert len(paper_tree.get_rectangles()) == 1
    assert paper_tree.get_tree_at_position((0, 0)) is not None
    paper_tree.update_data_sizes()
    paper_tree.expand_all()

    # rest tested on the visualizer


# def test_parent_tree_attributes_empty() -> None:
#     """Test if PaperTree is set correctly This test will not work.
#     """
#     paper_tree = PaperTree('TEST', [], all_papers=True, by_year=False)
#     assert True
#     # tested through debugging


if __name__ == '__main__':
    import pytest

    pytest.main(['test_paper.py'])
