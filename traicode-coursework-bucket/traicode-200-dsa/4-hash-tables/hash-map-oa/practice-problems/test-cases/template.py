import unittest
import json
import sys
from io import StringIO

class StaticArrayException(Exception):
    """
    Custom exception for Static Array class.
    Any changes to this class are forbidden.
    """
    pass


class StaticArray:
    """
    Implementation of Static Array Data Structure.
    Implemented methods: get(), set(), length()

    Any changes to this class are forbidden.

    Even if you make changes to your StaticArray file and upload to Gradescope
    along with your assignment, it will have no effect. Gradescope uses its
    own StaticArray file (a replica of this one) and any extra submission of
    a StaticArray file is ignored.
    """

    def __init__(self, size: int = 10) -> None:
        """
        Create array of given size.
        Initialize all elements with values of None.
        If requested size is not a positive number,
        raise StaticArray Exception.
        """
        if size < 1:
            raise StaticArrayException('Array size must be a positive integer')

        # The underscore denotes this as a private variable and
        # private variables should not be accessed directly.
        # Use the length() method to get the size of a StaticArray.
        self._size = size

        # Remember, this is a built-in list and is used here
        # because Python doesn't have a fixed-size array type.
        # Don't initialize variables like this in your assignments!
        self._data = [None] * size

    def __iter__(self) -> None:
        """
        Disable iterator capability for StaticArray class.
        This means loops and aggregate functions like
        those shown below won't work:

        arr = StaticArray()
        for value in arr:     # will not work
        min(arr)              # will not work
        max(arr)              # will not work
        sort(arr)             # will not work
        """
        return None

    def __str__(self) -> str:
        """Override string method to provide more readable output."""
        return f"STAT_ARR Size: {self._size} {self._data}"

    def get(self, index: int):
        """
        Return value from given index position.
        Invalid index raises StaticArrayException.
        """
        if index < 0 or index >= self.length():
            raise StaticArrayException('Index out of bounds')
        return self._data[index]

    def set(self, index: int, value) -> None:
        """
        Store value at given index in the array.
        Invalid index raises StaticArrayException.
        """
        if index < 0 or index >= self.length():
            raise StaticArrayException('Index out of bounds')
        self._data[index] = value

    def __getitem__(self, index: int):
        """Enable bracketed indexing."""
        return self.get(index)

    def __setitem__(self, index: int, value: object) -> None:
        """Enable bracketed indexing."""
        self.set(index, value)

    def length(self) -> int:
        """Return length of the array (number of elements)."""
        return self._size

class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass

class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

# --------------------------REPLACE CODE----------------------------------

    #{{CODE}}

# --------------------------UNIT TESTS------------------------------------
class TestDynamicArray(unittest.TestCase):

    def test_resize_1(self):
        da = DynamicArray()
        # Test resize with new capacity greater than the current size
        da.resize(10)
        self.assertEqual(da.get_capacity(), 10, "Failed to resize to a larger capacity")
        # Test resize with new capacity smaller than the current size
        da.resize(5)
        self.assertEqual(da.get_capacity(), 5, "Failed to resize to a smaller capacity")

    def test_append_1(self):
        da = DynamicArray()
        # Test append to an empty array
        da.append(1)
        self.assertEqual(list(da), [1], "Failed to append to an empty array")
        # Test append to a non-empty array
        da.append(2)
        self.assertEqual(list(da), [1, 2], "Failed to append to a non-empty array")

    def test_insert_at_index_1(self):
        da = DynamicArray([1, 2, 3])
        # Test inserting at the beginning of the array
        da.insert_at_index(0, 0)
        self.assertEqual(list(da), [0, 1, 2, 3], "Failed to insert at the beginning of the array")
    
    def test_insert_at_index_2(self):
        da = DynamicArray([0, 1, 2, 3])
        # Test inserting in the middle of the array
        da.insert_at_index(2, 1.5)
        self.assertEqual(list(da), [0, 1, 1.5, 2, 3], "Failed to insert in the middle of the array")
        # Test inserting at the end of the array
        da.insert_at_index(5, 4)
        self.assertEqual(list(da), [0, 1, 1.5, 2, 3, 4], "Failed to insert at the end of the array")
        
    def test_remove_at_index_1(self):
        da = DynamicArray([1, 2, 3, 4, 5])
        # Test removing from the middle of the array
        da.remove_at_index(2)
        self.assertEqual(list(da), [1, 2, 4, 5], "Failed to remove from the middle of the array")
        # Test removing from the beginning of the array
        da.remove_at_index(0)
        self.assertEqual(list(da), [2, 4, 5], "Failed to remove from the beginning of the array")
        # Test removing from the end of the array
        da.remove_at_index(2)
        self.assertEqual(list(da), [2, 4], "Failed to remove from the end of the array")

def run_tests():
    # Create a dictionary to store test results
    test_report = {}
    print_output = {}

    class CustomTestRunner(unittest.TextTestResult):
        def startTest(self, test: unittest.TestCase) -> None:
            super().startTest(test)
            # Capture the print output
            self.captured_output = StringIO()
            sys.stdout = self.captured_output

        def stopTest(self, test: unittest.TestCase) -> None:
            super().stopTest(test)
            # print("Ending: ",test._testMethodName)
            sys.stdout = sys.__stdout__
            print_output[test._testMethodName] = self.captured_output.getvalue().strip()

        def addSuccess(self, test):
            super().addSuccess(test)
            test_name = test._testMethodName
            # if test_name not in test_report:
            #     test_report[test_name] = []
            test_report[test_name] = {"status": "success", "message": "Test passed"}

        def addFailure(self, test, err):
            super().addFailure(test, err)
            test_name = test._testMethodName
            
            # if test_name not in test_report:
            #     test_report[test_name] = []
            test_report[test_name] = {"status": "failure", "message": str(err[1])}

        def addError(self, test, err):
            super().addError(test, err)
            test_name = test._testMethodName
            # if test_name not in test_report:
            #     test_report[test_name] = []
            test_report[test_name] = {"status": "error", "message": str(err[1])}

    def create_test_suite():
        suite = unittest.TestSuite()
        suite.addTest(TestDynamicArray("test_resize_1"))
        suite.addTest(TestDynamicArray("test_append_1"))
        suite.addTest(TestDynamicArray("test_insert_at_index_1"))
        suite.addTest(TestDynamicArray("test_insert_at_index_2"))
        suite.addTest(TestDynamicArray("test_remove_at_index_1"))
        return suite

    # Create the test suite
    test_suite = create_test_suite()

    # Run the test suite with custom test runner
    runner = unittest.TextTestRunner(resultclass=CustomTestRunner, stream=sys.stdout).run(test_suite)

    # Merge the print_output and test_report
    for key in print_output:
        test_report[key]["stdout"] = print_output[key]

    # Convert the test results to JSON string
    json_report = json.dumps(test_report)
    return json_report

if __name__ == "__main__":
    # Run the tests and get the JSON report
    json_report = run_tests()
    print("****TEST_REPORT****")
    print(json_report)