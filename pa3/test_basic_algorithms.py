# CS121: Analyzing Election Tweets
# 
# Test code for basic analysis algorithms
#

from basic_algorithms import find_top_k, find_min_count, find_frequent
import pytest
import os
import sys

# Handle the fact that the grading code may not
# be in the same directory as schelling.py
sys.path.append(os.getcwd())

# Get the test files from the same directory as
# this file.
BASE_DIR = os.path.dirname(__file__)

def helper(test_name, test_fn, input0, input1, expected_result):
    print(input0)
    print(input1)
    print(expected_result)
    try:
        actual_result = test_fn(input0, input1)
    # add something to name exception
    except Exception as e:
        
        s = "Test {}: caught exception: {}"
        pytest.fail(s.format(test_name, e))
        return

    if actual_result != expected_result:
        print("actual", actual_result)
        print("expected", expected_result)
        if len(actual_result) != len(expected_result):
            s = "Test {}: Length of actual result ({}) does not match the length of the expected result ({})"
            pytest.fail(s.format(test_name, len(actual_result), len(expected_result)))
        else:
            for i in range(len(actual_result)):
                print(i)
                if actual_result[i] != expected_result[i]:
                    s = "Test {} failed:"
                    s = s + "  Actual and expected results do not match.  First difference at index {}.\n"
                    s = s + "  Actual result: {}\n"
                    s = s + "  Expected result: {}\n"
                    pytest.fail(s.format(test_name, actual_result, expected_result))

            
############### top-k tests ###############
def test_top_k_0():
    # Check empty list
    helper("top_k_0", find_top_k, [], 1, [])

def test_top_k_1():
    # Check list with one item
    helper("top_k_1", find_top_k, ["A"], 1, [("A", 1)])

def test_top_k_2():
    # Check list with multiple unique values and K less than the
    # number of unique values.  'B' and 'C' have the same number of
    # occurrences.  Both 'B' and 'C' should be in the result.
    l = ['A', 'B', 'C', 'A', 'A', 'B', 'A', 'C', 'A', 'D']
    helper("top_k_6", find_top_k, l, 3, [('A', 5), ('B', 2), ('C', 2)])


############### min count tests ###############

def test_min_count_0():
    # Check empty list
    helper("min_count_0", find_min_count, [], 1, [])

def test_min_count_1():
    # Check list with one unique value that occurs three times and min_count of 3
    helper("min_count_3", find_min_count, ["A", "A", "A"], 3, [("A", 3)])

def test_min_count_2():
    # Check list with one unique value and min_count of 4, which will yield an empty list.
    helper("min_count_4", find_min_count, ["A", "A", "A"], 4, [])
    
def test_min_count_3():
    # Check list with multiple unique values and min_count of 2.  Note
    # that two of the items occur twice.
    l = ['A', 'B', 'C', 'A', 'A', 'B', 'A', 'C', 'A', 'D']
    helper("min_count_5", find_min_count, l, 2, [('A', 5), ('B', 2), ('C', 2)])


############### frequent tests ###############
def test_frequent_0():
    # Check empty list
    helper("frequent_0", find_frequent, [], 1, [])

def test_frequent_1():
    # Check list with one item and K of 2
    helper("frequent_1", find_frequent, ["A"], 2, [("A", 1)])

def test_frequent_2():
    # Check list with one unique value and K of 10
    helper("frequent_2", find_frequent, ["A", "A", "A"], 10, [("A", 3)])

def test_frequent_3():
    l = ["A", "A", "B", "B", "A", "B", "C", "B", "A"]
    helper("frequent_3", find_frequent, l, 3, [('A', 3), ('B', 3)])

def test_frequent_4():
    # Check list with multiple unique values and K of 3.
    l = ['A', 'B', 'C', 'A', 'A', 'B', 'A', 'C', 'A', 'D']
    helper("frequent_3", find_frequent, l, 3, [('A', 3), ('D', 1)])

def test_frequent_5():
    # Check list with multiple unique values and K of 5.
    l = ['A', 'B', 'C', 'A', 'A', 'B', 'A', 'C', 'A', 'D']
    helper("frequent_4", find_frequent, l, 5, [('A', 5), ('B', 2), ('C', 2), ('D', 1)])

def test_frequent_6():
    # Check list with multiple unique values and K of 2.  None of the
    # values occur more than half the time.  The data structure has a
    # count of 1 associated when "A" when it encounters the string "D".  As a
    # result, it has zero keys after processing the string "D".

    l = ['A', 'B', 'C', 'A', 'A', 'B', 'A', 'C', 'A', 'D']
    helper("frequent_5", find_frequent, l, 2, [])


