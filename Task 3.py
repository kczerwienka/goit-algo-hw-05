import timeit 
import numpy as np

s1 = "Engineering" # string existing in the text
s2 = "test"        # made up string

with open('article 1.txt', "r", encoding="utf8") as f:
    a1 = f.read()

with open('article 2.txt', "r", encoding="utf8") as f:
    a2 = f.read()


def boyer_moore_search(text, pattern):
    
    def build_shift_table(pattern):
        """Create a shift table for the Boyer-Moore algorithm."""
        table = {}
        length = len(pattern)
        # For each character in the substring, set the offset equal to the length of the substring
        for index, char in enumerate(pattern[:-1]):
            table[char] = length - index - 1
        # If the character is not in the table, the offset will be equal to the length of the substring
        table.setdefault(pattern[-1], length)
        return table
    
    # Create a shift table for the pattern (substring)
    shift_table = build_shift_table(pattern)
    i = 0 # Initialize the starting index for the main text

    # We go through the main text, comparing it with the substring
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1 # Start from the end of the substring

        # Compare characters from the end of the substring to the beginning
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1 # Shift to the beginning of the substring

        # If the entire substring matches, return its position in the text
        if j < 0:
            return i # String found

        # Shift the index i based on the offset table
        # This allows you to "jump" over mismatched parts of the text
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

    # If the substring is not found, return -1
    return -1


def kmp_search(main_string, pattern):

    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1

        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1

        return lps

    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1 # if a substring is not found


def rabin_karp_search(main_string, substring):
    
    def polynomial_hash(s, base=256, modulus=101):
        """
    Returns a polynomial hash of the string s.
        """
        n = len(s)
        hash_value = 0
        for i, char in enumerate(s):
            power_of_base = pow(base, n - i - 1) % modulus
            hash_value = (hash_value + ord(char) * power_of_base) % modulus
        return hash_value

    # lengths of main string and search substring
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Base number for hashing and module
    base = 256 
    modulus = 101  
    
    # Hash value for the search substring and the current segment in the main string
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Previous value for hash recalculation
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Going through the main string
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

results = np.zeros((3, 4))
label = np.array([["boyer_moore_search"], ["kmp_search"], ["rabin_karp_search"]]) 


results[0, 0] = timeit.timeit("boyer_moore_search(a1, s1)", setup="from __main__ import boyer_moore_search, a1, s1, a2, s2", number=10000)
results[0, 1] = timeit.timeit("boyer_moore_search(a2, s1)", setup="from __main__ import boyer_moore_search, a1, s1, a2, s2", number=10000)
results[0, 2] = timeit.timeit("boyer_moore_search(a1, s2)", setup="from __main__ import boyer_moore_search, a1, s1, a2, s2", number=10000)
results[0, 3] = timeit.timeit("boyer_moore_search(a2, s2)", setup="from __main__ import boyer_moore_search, a1, s1, a2, s2", number=10000)

results[1, 0] = timeit.timeit("kmp_search(a1, s1)", setup="from __main__ import kmp_search, a1, s1, a2, s2", number=10000)
results[1, 1] = timeit.timeit("kmp_search(a2, s1)", setup="from __main__ import kmp_search, a1, s1, a2, s2", number=10000)
results[1, 2] = timeit.timeit("kmp_search(a1, s2)", setup="from __main__ import kmp_search, a1, s1, a2, s2", number=10000)
results[1, 3] = timeit.timeit("kmp_search(a2, s2)", setup="from __main__ import kmp_search, a1, s1, a2, s2", number=10000)

results[2, 0] = timeit.timeit("rabin_karp_search(a1, s1)", setup="from __main__ import rabin_karp_search, a1, s1, a2, s2", number=10000)
results[2, 1] = timeit.timeit("rabin_karp_search(a2, s1)", setup="from __main__ import rabin_karp_search, a1, s1, a2, s2", number=10000)
results[2, 2] = timeit.timeit("rabin_karp_search(a1, s2)", setup="from __main__ import rabin_karp_search, a1, s1, a2, s2", number=10000)
results[2, 3] = timeit.timeit("rabin_karp_search(a2, s2)", setup="from __main__ import rabin_karp_search, a1, s1, a2, s2", number=10000)

print(label,)
print(results)