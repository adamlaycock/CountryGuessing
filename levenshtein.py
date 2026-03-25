#Compute the Levenshtein distance between two strings to allow for typos
#We can calculate how close the user input is to any correct country (not optimised) (womp womp i guess)

def levenshtein_distance(str1, str2):
    len_str1 = len(str1) + 1
    len_str2 = len(str2) + 1
    dp = [[0] * len_str2 for _ in range(len_str1)]

    # Initialize the matrix
    for i in range(len_str1):
        dp[i][0] = i
    for j in range(len_str2):
        dp[0][j] = j

    # Compute the Levenshtein distance
    for i in range(1, len_str1):
        for j in range(1, len_str2):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,     # Deletion
                dp[i][j - 1] + 1,     # Insertion
                dp[i - 1][j - 1] + cost  # Substitution
            )

    return dp[len_str1 - 1][len_str2 - 1]
