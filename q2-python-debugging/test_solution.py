import sys
from pathlib import Path

# Add current folder to sys.path so solution can always be imported regardless of execution working directory
sys.path.insert(0, str(Path(__file__).resolve().parent))

from solution import find_duplicates


def test_assessment_example():
    """Verify the exact assessment example: [1, 2, 3, 2, 4, 1, 5, 2] -> [1, 2]."""
    items = [1, 2, 3, 2, 4, 1, 5, 2]
    assert find_duplicates(items) == [1, 2]


def test_no_duplicates():
    """Verify list with all unique elements returns empty list."""
    assert find_duplicates([1, 2, 3]) == []


def test_string_values():
    """Verify list with string elements returns duplicates in preserved order."""
    items = ["a", "b", "a", "c", "b"]
    assert find_duplicates(items) == ["a", "b"]


def test_multiple_occurrences_of_same_value():
    """Verify elements appearing many times are included only once."""
    assert find_duplicates([5, 5, 5, 5]) == [5]


def test_empty_list():
    """Verify empty list returns an empty list."""
    assert find_duplicates([]) == []


def test_duplicate_integers_order_preserved():
    """Verify order of first occurrence is preserved for duplicates."""
    items = [10, 20, 30, 20, 10, 40]
    assert find_duplicates(items) == [10, 20]


def test_input_list_remains_unchanged():
    """Verify the original input list is not mutated."""
    original = [1, 2, 3, 2, 4, 1, 5, 2]
    copy = list(original)
    result = find_duplicates(original)
    assert result == [1, 2]
    assert original == copy
