from difflib import SequenceMatcher as SM


def is_match(s1, s2):
    """
    Fuzzy matching of two strings
    Return True if probability of match is at least 80%
    """
    return SM(None, s1, s2).ratio() >= 0.80
