from collections import defaultdict


def array_to_dict(arr):
    counts = defaultdict(int)
    for num in arr:
        counts[num] += 1
    return dict(counts)


# compares the values between two dictionaries
def compare_dict_values(dict1, dict2):
    for key in dict1:
        if key not in dict2 or dict1[key] > dict2[key]:
            return False
    return True
