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
