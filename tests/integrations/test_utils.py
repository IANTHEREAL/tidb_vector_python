"""Test TiDB Vector Search functionality."""
from __future__ import annotations

from tidb_vector.integrations.utils import extract_info_from_column_definition


def test_extract_info_from_column_definition():
    # Test case with dimension and distance metric
    column_type = "VECTOR<FLOAT>(128) COMMENT 'hnsw(distance=cosine)'"
    expected_result = (128, "cosine")
    assert extract_info_from_column_definition(column_type) == expected_result

    # Test case with dimension but no distance metric
    column_type = "VECTOR<FLOAT>(256) COMMENT 'some comment'"
    expected_result = (256, None)
    assert extract_info_from_column_definition(column_type) == expected_result

    # Test case with no dimension and no distance metric
    column_type = "VECTOR<FLOAT> COMMENT 'another comment'"
    expected_result = (None, None)
    assert extract_info_from_column_definition(column_type) == expected_result

    # Test case with no dimension and no comment
    column_type = "VECTOR<FLOAT>"
    expected_result = (None, None)
    assert extract_info_from_column_definition(column_type) == expected_result

    # Test case with dimension but no comment
    column_type = "VECTOR<FLOAT>"
    expected_result = (None, None)
    assert extract_info_from_column_definition(column_type) == expected_result

    # Test normal case with double quotes
    column_type = 'VECTOR<FLOAT>(128) COMMENT "hnsw(distance=cosine)"'
    expected_result = (128, "cosine")
    assert extract_info_from_column_definition(column_type) == expected_result

    # Test case with single quotes without index type
    column_type = "VECTOR<FLOAT> COMMENT 'distance=l2'"
    expected_result = (None, "l2")
    assert extract_info_from_column_definition(column_type) == expected_result

    # Test case with addition comment content
    column_type = "VECTOR<FLOAT>(128) COMMENT 'test, hnsw(distance=l2)'"
    expected_result = (128, "l2")
    assert extract_info_from_column_definition(column_type) == expected_result
