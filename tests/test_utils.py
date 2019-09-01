import pytest
from version_control.lcs import lcs_multi_dimension, inserted_paths


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


def test_column_all():
    A = [[["A"], ["B"]], [["C"], ["D"]]]
    B = [[["A", "X"], ["B", "Y"]], [["C", "Q"], ["D", "K"]]]

    dim_matches = lcs_multi_dimension(A, B, 3)
    inserted_rows, inserted_cols = inserted_paths(A, B, dim_matches)
    print(inserted_paths(A, B, dim_matches))

    assert len(inserted_rows) == 0
    assert len(inserted_cols) == 1
    assert inserted_cols[0] == ["_", "_", 1]
