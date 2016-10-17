import sys

# Implement a function called negate_values here
# This function takes a list of integers, and returns
# a *new* list with the values of the list negated.


if __name__ == "__main__":
    # parse the input
    l = [int(item.strip()) for item in sys.stdin.read().split()]

    l_copy = l[:]

    # Replace l with a call to your negate_values function
    # Variable l contains the list of integers.
    rv = l

    if l != l_copy:
        raise ValueError("Don't modify the list you pass to negate_values!")

    print(" ".join([str(x) for x in rv]))
