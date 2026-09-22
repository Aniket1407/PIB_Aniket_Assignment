import sys
from pathlib import Path

# Ensure this directory is prioritized and local solution module is loaded
current_dir = str(Path(__file__).resolve().parent)
sys.path.insert(0, current_dir)
if "solution" in sys.modules and getattr(sys.modules["solution"], "__file__", "") != str(Path(current_dir) / "solution.py"):
    del sys.modules["solution"]

from solution import (
    calculate_statistics,
    get_top_users,
    load_users,
    process_users,
    run_pipeline,
)


def test_normal_input():
    """Verify processing with standard valid records."""
    users = [
        {"user_id": "U1", "name": "Alice", "age": 20, "score": 70},
        {"user_id": "U2", "name": "Bob", "age": 25, "score": 80},
    ]
    valid = process_users(users)
    assert len(valid) == 2
    assert [u["user_id"] for u in valid] == ["U1", "U2"]


def test_duplicate_user_ids():
    """Verify duplicate user IDs are deduplicated."""
    users = [
        {"user_id": "U1", "name": "Alice", "age": 20, "score": 75},
        {"user_id": "U1", "name": "Alice Copy", "age": 20, "score": 75},
        {"user_id": "U2", "name": "Bob", "age": 22, "score": 85},
    ]
    valid = process_users(users)
    assert len(valid) == 2
    assert [u["user_id"] for u in valid] == ["U1", "U2"]


def test_first_duplicate_occurrence_is_retained():
    """Verify that the first occurrence of a duplicate record is kept, not later ones."""
    users = [
        {"user_id": "U1", "name": "First Instance", "age": 20, "score": 60},
        {"user_id": "U1", "name": "Second Instance", "age": 20, "score": 90},
    ]
    valid = process_users(users)
    assert len(valid) == 1
    assert valid[0]["name"] == "First Instance"
    assert valid[0]["score"] == 60


def test_score_below_50_is_removed():
    """Verify users with score < 50 are filtered out."""
    users = [
        {"user_id": "U1", "name": "Alice", "age": 20, "score": 49},
        {"user_id": "U2", "name": "Bob", "age": 22, "score": 30},
        {"user_id": "U3", "name": "Charlie", "age": 25, "score": 55},
    ]
    valid = process_users(users)
    assert len(valid) == 1
    assert valid[0]["user_id"] == "U3"


def test_score_exactly_50_is_retained():
    """Verify score of exactly 50 is included in the valid dataset."""
    users = [
        {"user_id": "U1", "name": "Threshold User", "age": 24, "score": 50},
    ]
    valid = process_users(users)
    assert len(valid) == 1
    assert valid[0]["score"] == 50


def test_average_score():
    """Verify average score calculation and rounding to 2 decimal places."""
    users = [
        {"user_id": "U1", "name": "A", "score": 70},
        {"user_id": "U2", "name": "B", "score": 75},
        {"user_id": "U3", "name": "C", "score": 82},
    ]
    # (70 + 75 + 82) / 3 = 227 / 3 = 75.6666... -> 75.67
    stats = calculate_statistics(users)
    assert stats["average_score"] == 75.67


def test_maximum_score():
    """Verify max score calculation."""
    users = [
        {"user_id": "U1", "score": 60},
        {"user_id": "U2", "score": 95},
        {"user_id": "U3", "score": 70},
    ]
    stats = calculate_statistics(users)
    assert stats["max_score"] == 95


def test_minimum_score():
    """Verify min score calculation."""
    users = [
        {"user_id": "U1", "score": 60},
        {"user_id": "U2", "score": 95},
        {"user_id": "U3", "score": 52},
    ]
    stats = calculate_statistics(users)
    assert stats["min_score"] == 52


def test_top_10_users_limit_enforced():
    """Verify exactly 10 users are returned when there are more than 10 valid records."""
    users = [{"user_id": f"U{i}", "name": f"User {i}", "score": 50 + i} for i in range(15)]
    top = get_top_users(users, limit=10)
    assert len(top) == 10
    # Top user should have the highest score (50 + 14 = 64)
    assert top[0]["score"] == 64
    assert top[-1]["score"] == 55


def test_fewer_than_10_valid_users():
    """Verify all valid users are returned when count is less than 10."""
    users = [
        {"user_id": "U1", "score": 80},
        {"user_id": "U2", "score": 90},
        {"user_id": "U3", "score": 70},
    ]
    top = get_top_users(users, limit=10)
    assert len(top) == 3
    assert [u["score"] for u in top] == [90, 80, 70]


def test_empty_input():
    """Verify processing and statistics on empty input dataset."""
    valid = process_users([])
    assert valid == []

    stats = calculate_statistics([])
    assert stats == {"average_score": 0, "max_score": 0, "min_score": 0}

    top = get_top_users([], limit=10)
    assert top == []


def test_all_records_filtered_out():
    """Verify dataset where all users have scores < 50."""
    users = [
        {"user_id": "U1", "score": 20},
        {"user_id": "U2", "score": 45},
        {"user_id": "U3", "score": 10},
    ]
    valid = process_users(users)
    assert valid == []

    stats = calculate_statistics(valid)
    assert stats == {"average_score": 0, "max_score": 0, "min_score": 0}

    top = get_top_users(valid, limit=10)
    assert top == []


def test_duplicate_records_with_different_scores():
    """
    Verify duplicate records with conflicting scores:
    First record is kept; second record is skipped.
    """
    users = [
        {"user_id": "U1", "name": "First Score 80", "score": 80},
        {"user_id": "U1", "name": "Later Score 95", "score": 95},
        {"user_id": "U2", "name": "First Below 50", "score": 40},
        {"user_id": "U2", "name": "Later Above 50", "score": 75},
    ]
    valid = process_users(users)
    # U1: first score is 80 (kept)
    # U2: first score is 40 (<50, filtered out); second score 75 is skipped because user_id was already seen
    assert len(valid) == 1
    assert valid[0]["user_id"] == "U1"
    assert valid[0]["score"] == 80


def test_top_10_sorted_descending():
    """Verify top 10 users are sorted in strictly non-increasing score order."""
    users = [
        {"user_id": "U1", "score": 65},
        {"user_id": "U2", "score": 95},
        {"user_id": "U3", "score": 75},
        {"user_id": "U4", "score": 85},
        {"user_id": "U5", "score": 55},
    ]
    top = get_top_users(users, limit=10)
    scores = [u["score"] for u in top]
    assert scores == [95, 85, 75, 65, 55]
    assert scores == sorted(scores, reverse=True)


def test_end_to_end_with_sample_data_file():
    """Verify end-to-end execution against the provided data.json file."""
    data_path = Path(__file__).resolve().parent / "data.json"
    result = run_pipeline(data_path)

    assert result["total_input_records"] == 17
    assert result["valid_records_count"] == 13
    assert len(result["top_users"]) == 10

    # Ensure max and min match valid records
    assert result["statistics"]["max_score"] == 95
    assert result["statistics"]["min_score"] == 50
    assert result["statistics"]["average_score"] == 76.54

    # Ensure top users are sorted descending
    top_scores = [u["score"] for u in result["top_users"]]
    assert top_scores == sorted(top_scores, reverse=True)
