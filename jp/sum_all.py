
def sum_all(l):
    """
    This function takes a nested list of integers and returns the sum of all integers in the list.
    It uses recursion to handle nested lists.
    """
    total = 0
    for item in l:
        if isinstance(item, list):
            total += sum_all(item)
        else:
            total += item
    return total




def kakla():
    print("ROFLAMAO")



def test_sum_all(l,e):
    try:
        r = sum_all(l)
        if r == e:
            return 'OK'
        return 'Fail! Expected: ' + str(e) + ' but got: ' + str(r)
    except Exception as ex:
        return 'Error: ' + str(ex)
    
print(test_sum_all([1, [2, 3], 4, [5, [6, 7]]], 28))
print(test_sum_all([[1, 2], [3, [4]], 5, 6], 21))
print(test_sum_all([10, [20, [30, 40]], 50], 150))
print(test_sum_all([[[[1]]], 2, 3, [4, 5]], 15))
print(test_sum_all([0, [1, [2, [3, [4]]]]], 10))
print(test_sum_all([[1], [2], [3], [4, [5, [6]]]], 21))
print(test_sum_all([100, [200], [300, [400, [500]]]], 1500))
print(test_sum_all([[1, 2, [3]], [4, [5, [6]]], 7], 28))
print(test_sum_all([5, [10, [15, 20], 25], 30], 105))
print(test_sum_all([[0], [[1], [[2], [[3], [4]]]]], 10))
