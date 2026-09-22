import json
import sys
from pathlib import Path


def load_users(file_path):
    """
    Load user records from a JSON file.
    Returns an empty list if file is empty or not found.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Expected a list of user objects in JSON file")
        return data


def process_users(users):
    """
    Process records by:
    1. Tracking seen user IDs in a set.
    2. Keeping the FIRST occurrence of any user_id and skipping later duplicates.
    3. Filtering out records where score < 50 (scores >= 50 are retained).

    Time Complexity: O(n) where n is the number of records.
    Space Complexity: O(u) where u is the number of unique user IDs.
    """
    seen_user_ids = set()
    valid_users = []

    for user in users:
        user_id = user.get("user_id")
        if user_id in seen_user_ids:
            continue

        seen_user_ids.add(user_id)

        score = user.get("score", 0)
        if score >= 50:
            valid_users.append(user)

    return valid_users


def calculate_statistics(users):
    """
    Calculate average, maximum, and minimum score from the valid users.
    Returns zeroes if the dataset is empty.
    """
    if not users:
        return {
            "average_score": 0,
            "max_score": 0,
            "min_score": 0,
        }

    scores = [u["score"] for u in users]
    avg_score = round(sum(scores) / len(scores), 2)

    return {
        "average_score": avg_score,
        "max_score": max(scores),
        "min_score": min(scores),
    }


def get_top_users(users, limit=10):
    """
    Return up to `limit` users sorted by score in descending order.
    Preserves input order for users with identical scores (Python's stable sort).
    """
    return sorted(users, key=lambda u: u["score"], reverse=True)[:limit]


def run_pipeline(file_path="data.json"):
    """
    Execute the end-to-end data processing pipeline for a given JSON file.
    """
    users = load_users(file_path)
    valid_users = process_users(users)
    stats = calculate_statistics(valid_users)
    top_10 = get_top_users(valid_users, limit=10)

    return {
        "total_input_records": len(users),
        "valid_records_count": len(valid_users),
        "statistics": stats,
        "top_users": top_10,
    }


if __name__ == "__main__":
    target_file = sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent / "data.json"
    result = run_pipeline(target_file)
    print("=== Python Data Processing Summary ===")
    print(f"Total Input Records : {result['total_input_records']}")
    print(f"Valid Records Count : {result['valid_records_count']}")
    print("\n--- Statistics ---")
    print(f"Average Score       : {result['statistics']['average_score']}")
    print(f"Maximum Score       : {result['statistics']['max_score']}")
    print(f"Minimum Score       : {result['statistics']['min_score']}")
    print(f"\n--- Top {len(result['top_users'])} Users ---")
    for idx, u in enumerate(result["top_users"], start=1):
        print(f"{idx:2d}. {u['name']} (ID: {u['user_id']}, Age: {u['age']}) -> Score: {u['score']}")
