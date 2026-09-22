def find_duplicates(items):
    """
    Find duplicate elements in a list, returning each duplicate only once,
    preserving the order of their first appearance.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1

    duplicates = []
    seen = set()

    for item in items:
        if counts[item] > 1 and item not in seen:
            seen.add(item)
            duplicates.append(item)

    return duplicates


if __name__ == "__main__":
    sample_list = [1, 2, 3, 2, 4, 1, 5, 2]
    result = find_duplicates(sample_list)
    print("=" * 45)
    print("      QUESTION 2: FIND DUPLICATES")
    print("=" * 45)
    print(f"Input List  : {sample_list}")
    print(f"Duplicates  : {result}")

    sample_strings = ["apple", "banana", "apple", "orange", "banana"]
    print(f"\nStrings List: {sample_strings}")
    print(f"Duplicates  : {find_duplicates(sample_strings)}")
    print("=" * 45)
