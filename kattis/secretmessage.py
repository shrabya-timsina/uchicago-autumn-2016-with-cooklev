import sys

# Skeleton code for problem https://uchicago.kattis.com/problems/secretmessage
#
# Make sure you read the problem before editing this code.
#
# You should focus only on implementing the solve() function.
# Do not modify any other code.

import math

def solve(message):
    """
    Parameters:
     - message: String. The message.

    Returns: String. The secret message
    """
    L = len(message)
    M = int(math.ceil(math.sqrt(L)))
    
    table = [ [0]*M for _ in range(M) ]
    k = 0
    for i in range(M):
        for j in range(M):
            if k < L:
                table[i][j] = message[k]
                k += 1
            else:
                table[i][j] = "*"

    secret_message = ""
    for j in range(M):
        for i in range(M-1,-1,-1):
            if table[i][j] != "*":
                secret_message += table[i][j]

    return secret_message        

    # YOUR CODE HERE

    # Replace "" with your return value
    return ""


if __name__ == "__main__":
    tokens = sys.stdin.read().strip().split()
    tokens.reverse()

    m = int(tokens.pop())

    for i in range(m):
        message = tokens.pop()
        secret_message = solve(message)
        assert isinstance(secret_message, str), "solve() should return a string"
        print(secret_message)        
