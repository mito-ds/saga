import pytest
from saga.data_types.multi_dim_list.lcs import lcs_multi_dimension, inserted_paths, removed_paths, changed_paths


def test_basic_col_add():
    A = [["A", "B"], ["C", "D"]]
    B = [["A", "B", "X"], ["C", "D", "Y"]]

    dim_matches = lcs_multi_dimension(A, B, 2)
    inserted_rows, inserted_cols = inserted_paths(A, B, dim_matches)

    assert len(inserted_rows) == 0
    assert len(inserted_cols) == 1
    assert inserted_cols[0][0] == "_"
    assert inserted_cols[0][1] == 2

def test_basic_row_add():
    A = [["A", "B"], ["C", "D"]]
    B = [["A", "B"], ["C", "D"], ["E", "F"]]

    dim_matches = lcs_multi_dimension(A, B, 2)
    inserted_rows, inserted_cols = inserted_paths(A, B, dim_matches)

    assert len(inserted_rows) == 1
    assert len(inserted_cols) == 0
    assert inserted_rows[0][0] == 2


def test_column_add_unification():
    A = [[["A"], ["B"]], [["C"], ["D"]]]
    B = [[["A", "X"], ["B", "Y"]], [["C", "Q"], ["D", "K"]]]

    dim_matches = lcs_multi_dimension(A, B, 3)
    inserted_rows, inserted_cols = inserted_paths(A, B, dim_matches)
    print(inserted_paths(A, B, dim_matches))

    assert len(inserted_rows) == 0
    assert len(inserted_cols) == 1
    assert inserted_cols[0] == ["_", "_", 1]


def test_remove_row():
    A = [["A", "B"], ["C", "D"]]
    B = [["A", "B"]]

    dim_matches = lcs_multi_dimension(A, B, 2)
    removed_rows, removed_cols = removed_paths(A, B, dim_matches)

    assert len(removed_rows) == 1
    assert len(removed_cols) == 0
    assert removed_rows[0] == [1]

def remove_column():
    A = [["A", "B"], ["C", "D"]]
    B = [["A"], ["C"]]

    dim_matches = lcs_multi_dimension(A, B, 2)
    removed_rows, removed_cols = removed_paths(A, B, dim_matches)

    assert len(removed_rows) == 0
    assert len(removed_cols) == 1
    assert removed_cols[0] == [1]

def test_column_remove_unification():
    A = [[["A", "X"], ["B", "Y"]], [["C", "Q"], ["D", "K"]]]
    B = [[["A"], ["B"]], [["C"], ["D"]]]

    dim_matches = lcs_multi_dimension(A, B, 3)
    removed_rows, removed_cols = removed_paths(A, B, dim_matches)

    assert len(removed_rows) == 0
    assert len(removed_cols) == 1
    assert removed_cols[0] == ["_", "_", 1]


def test_change_value_total():
    # a total change is a remove then an insert
    A = [["A", "B"], ["C", "D"]]
    B = [["A", "B"], ["C", "E"]]

    dim_matches = lcs_multi_dimension(A, B, 2)
    paths = changed_paths(A, B, dim_matches)
    removed_rows, removed_cols = removed_paths(A, B, dim_matches)
    inserted_rows, inserted_cols = inserted_paths(A, B, dim_matches)

    assert len(paths) == 0 
    assert len(removed_rows) == 1
    assert len(removed_cols) == 0
    assert len(inserted_rows) == 1
    assert len(inserted_cols) == 0
    assert removed_rows[0] == [1, 1]
    assert inserted_rows[0] == [1, 1]



def test_change_value_partial():
    # a partial change is just a change
    A = [["A", "B"], ["C", "DE"]]
    B = [["A", "B"], ["C", "E"]]

    dim_matches = lcs_multi_dimension(A, B, 2)
    paths = changed_paths(A, B, dim_matches)
    removed_rows, removed_cols = removed_paths(A, B, dim_matches)
    inserted_rows, inserted_cols = inserted_paths(A, B, dim_matches)

    assert len(paths) == 1
    assert paths[0] == [1, 1]
    assert len(removed_rows) == 0
    assert len(removed_cols) == 0
    assert len(inserted_rows) == 0
    assert len(inserted_cols) == 0


def test_delete_non_rectangular():
    A = [["A", "B"], ["C", "E"]]
    B = [["A"], ["C", "E"]]

    dim_matches = lcs_multi_dimension(A, B, 2)
    paths = changed_paths(A, B, dim_matches)
    removed_rows, removed_cols = removed_paths(A, B, dim_matches)
    inserted_rows, inserted_cols = inserted_paths(A, B, dim_matches)

    assert len(paths) == 0
    assert len(removed_rows) == 1
    assert removed_rows[0] == [0, 1]
    assert len(removed_cols) == 0
    assert len(inserted_rows) == 0
    assert len(inserted_cols) == 0


def test_delete_non_rectangular_col():
    A = [["A", "B"], ["C"]]
    B = [["A"], ["C"]]

    dim_matches = lcs_multi_dimension(A, B, 2)
    paths = changed_paths(A, B, dim_matches)
    removed_rows, removed_cols = removed_paths(A, B, dim_matches)
    inserted_rows, inserted_cols = inserted_paths(A, B, dim_matches)

    assert len(paths) == 0
    assert len(removed_rows) == 0
    assert len(removed_cols) == 1
    assert removed_cols[0] == ["_", 1]
    assert len(inserted_rows) == 0
    assert len(inserted_cols) == 0


def test_add_row_and_column():
    A = [["A"], ["C"]]
    B = [["A", "B"], ["C", "D"], ["E", "F"]]

    dim_matches = lcs_multi_dimension(A, B, 2)
    paths = changed_paths(A, B, dim_matches)
    removed_rows, removed_cols = removed_paths(A, B, dim_matches)
    inserted_rows, inserted_cols = inserted_paths(A, B, dim_matches)

    assert len(paths) == 0
    assert len(removed_rows) == 0
    assert len(removed_cols) == 0
    assert len(inserted_rows) == 1
    assert len(inserted_cols) == 1

    
