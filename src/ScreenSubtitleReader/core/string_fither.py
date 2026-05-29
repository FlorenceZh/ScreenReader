from Levenshtein import ratio

def is_similar_str(str1,str2)->bool:
    result = ratio(str1,str2) > 0.85
    return result