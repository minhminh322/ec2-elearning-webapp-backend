import unittest
import json
import sys
from io import StringIO

class DynamicArrayException(Exception):
    pass


class DynamicArray:
    def __init__(self, arr=None) -> None:
        self._data = arr.copy() if arr else []

    def __iter__(self):
        return None

    def __str__(self) -> str:
        """Override string method to provide more readable output."""
        return str(self._data)

    def append(self, value: object) -> None:
        """Add new element at the end of the array."""
        self._data.append(value)

    def pop(self):
        """Remove element from end of the array and return it."""
        return self._data.pop()

    def swap(self, i: int, j: int) -> None:
        """Swap two elements in array given their indices."""
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def get_at_index(self, index: int):
        """Return value of element at a given index."""
        if index < 0 or index >= self.length():
            raise DynamicArrayException
        return self._data[index]

    def __getitem__(self, index: int):
        """Return value of element at a given index using [] syntax."""
        return self.get_at_index(index)

    def set_at_index(self, index: int, value: object) -> None:
        """Set value of element at a given index."""
        if index < 0 or index >= self.length():
            raise DynamicArrayException
        self._data[index] = value

    def __setitem__(self, index: int, value: object) -> None:
        """Set value of element at a given index using [] syntax."""
        self.set_at_index(index, value)

    def length(self) -> int:
        """Return length of array."""
        return len(self._data)


def hash_function_1(key: str) -> int:
    """Sample Hash function #1 to be used with HashMap implementation"""
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """Sample Hash function #2 to be used with HashMap implementation"""
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash

class SLNode:
    def __init__(self, key: str, value: object, next: "SLNode" = None) -> None:
        """Initialize node given a key and value."""
        self.key = key
        self.value = value
        self.next = next

    def __str__(self) -> str:
        """Override string method to provide more readable output."""
        return '(' + str(self.key) + ': ' + str(self.value) + ')'


class LinkedListIterator:
    def __init__(self, current_node: SLNode) -> None:
        """Initialize the iterator with a node."""
        self._node = current_node

    def __iter__(self) -> "LinkedListIterator":
        """Return the iterator."""
        return self

    def __next__(self) -> SLNode:
        """Obtain next node and advance iterator."""

        if not self._node:
            raise StopIteration

        current_node = self._node
        self._node = self._node.next
        return current_node


class LinkedList:
    def __init__(self) -> None:
        """
        Initialize new linked list;
        doesn't use a sentinel and keeps track of its size in a variable.
        """
        self._head = None
        self._size = 0

    def __str__(self) -> str:
        """Override string method to provide more readable output."""
        if not self._head:
            return "SLL []"

        content = str(self._head)
        node = self._head.next
        while node:
            content += ' -> ' + str(node)
            node = node.next
        return 'SLL [' + content + ']'

    def __iter__(self) -> LinkedListIterator:
        """Return an iterator for the list, starting at the head."""
        return LinkedListIterator(self._head)

    def insert(self, key: str, value: object) -> None:
        """Insert new node at front of the list."""
        self._head = SLNode(key, value, self._head)
        self._size += 1

    def remove(self, key: str) -> bool:
        """
        Remove first node with matching key.
        Return True if removal was successful, False otherwise.
        """
        previous, node = None, self._head
        while node:

            if node.key == key:
                if previous:
                    previous.next = node.next
                else:
                    self._head = node.next
                self._size -= 1
                return True

            previous, node = node, node.next
        return False

    def contains(self, key: str) -> SLNode:
        """Return node with matching key, or None if no match"""
        node = self._head
        while node:
            if node.key == key:
                return node
            node = node.next
        return node

    def length(self) -> int:
        """Return the length of the list."""
        return self._size

class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        return self._size

    def get_capacity(self) -> int:
        return self._capacity

# --------------------------REPLACE CODE----------------------------------

    #{{CODE}}

# --------------------------UNIT TESTS------------------------------------
class TestHashMapSC(unittest.TestCase):

    def test_put_example_1(self):
        m = HashMap(53, hash_function_1)
        for i in range(150):
            m.put('str' + str(i), i * 100)
            if i % 25 == 24:
                self.assertEqual(m.empty_buckets(), 0)
                self.assertAlmostEqual(m.table_load(), 1.0, delta=0.01)
                self.assertEqual(m.get_size(), i + 1)
                self.assertEqual(m.get_capacity(), 53)

    def test_put_example_2(self):
        m = HashMap(41, hash_function_2)
        for i in range(50):
            m.put('str' + str(i // 3), i * 100)
            if i % 10 == 9:
                self.assertEqual(m.empty_buckets(), 0)
                self.assertAlmostEqual(m.table_load(), 1.0, delta=0.01)
                self.assertEqual(m.get_size(), i + 1)
                self.assertEqual(m.get_capacity(), 41)

    def test_resize_example_1(self):
        m = HashMap(20, hash_function_1)
        m.put('key1', 10)
        self.assertEqual(m.get_size(), 1)
        self.assertEqual(m.get_capacity(), 20)
        self.assertEqual(m.get('key1'), 10)
        self.assertTrue(m.contains_key('key1'))
        m.resize_table(30)
        self.assertEqual(m.get_size(), 1)
        self.assertEqual(m.get_capacity(), 30)
        self.assertEqual(m.get('key1'), 10)
        self.assertTrue(m.contains_key('key1'))

    def test_resize_example_2(self):
        m = HashMap(75, hash_function_2)
        keys = [i for i in range(1, 1000, 13)]
        for key in keys:
            m.put(str(key), key * 42)
        self.assertEqual(m.get_size(), len(keys))
        self.assertEqual(m.get_capacity(), 75)

        for capacity in range(111, 1000, 117):
            m.resize_table(capacity)

            m.put('some key', 'some value')
            self.assertTrue(m.contains_key('some key'))
            m.remove('some key')

            for key in keys:
                self.assertTrue(m.contains_key(str(key)))
                self.assertFalse(m.contains_key(str(key + 1)))
            self.assertAlmostEqual(m.table_load(), len(keys) / capacity, delta=0.01)

    def test_table_load_example_1(self):
        m = HashMap(101, hash_function_1)
        self.assertAlmostEqual(m.table_load(), 0.0, delta=0.01)
        m.put('key1', 10)
        self.assertAlmostEqual(m.table_load(), 0.01, delta=0.01)
        m.put('key2', 20)
        self.assertAlmostEqual(m.table_load(), 0.02, delta=0.01)
        m.put('key1', 30)
        self.assertAlmostEqual(m.table_load(), 0.02, delta=0.01)

    def test_table_load_example_2(self):
        m = HashMap(53, hash_function_1)
        for i in range(50):
            m.put('key' + str(i), i * 100)
            if i % 10 == 0:
                self.assertAlmostEqual(m.table_load(), (i + 1) / 53, delta=0.01)
                self.assertEqual(m.get_size(), i + 1)
                self.assertEqual(m.get_capacity(), 53)

    def test_empty_buckets_example_1(self):
        m = HashMap(101, hash_function_1)
        self.assertEqual(m.empty_buckets(), 101)
        m.put('key1', 10)
        self.assertEqual(m.empty_buckets(), 100)
        m.put('key2', 20)
        self.assertEqual(m.empty_buckets(), 99)
        m.put('key1', 30)
        self.assertEqual(m.empty_buckets(), 99)
        m.put('key4', 40)
        self.assertEqual(m.empty_buckets(), 98)

    def test_empty_buckets_example_2(self):
        m = HashMap(53, hash_function_1)
        for i in range(150):
            m.put('key' + str(i), i * 100)
            if i % 30 == 0:
                self.assertAlmostEqual(m.empty_buckets(), 53 - (i + 1), delta=1)

    def test_get_example_1(self):
        m = HashMap(31, hash_function_1)
        self.assertIsNone(m.get('key'))
        m.put('key1', 10)
        self.assertEqual(m.get('key1'), 10)

    def test_get_example_2(self):
        m = HashMap(151, hash_function_2)
        for i in range(200, 300, 7):
            m.put(str(i), i * 10)
        self.assertEqual(m.get_size(), 15)
        self.assertEqual(m.get_capacity(), 151)
        for i in range(200, 300, 21):
            self.assertEqual(m.get(str(i)), i * 10)
            self.assertTrue(m.get(str(i)) == i * 10)
            self.assertIsNone(m.get(str(i + 1)))

    def test_contains_key_example_1(self):
        m = HashMap(53, hash_function_1)
        self.assertFalse(m.contains_key('key1'))
        m.put('key1', 10)
        m.put('key2', 20)
        m.put('key3', 30)
        self.assertTrue(m.contains_key('key1'))
        self.assertFalse(m.contains_key('key4'))
        self.assertTrue(m.contains_key('key2'))
        self.assertTrue(m.contains_key('key3'))
        m.remove('key3')
        self.assertFalse(m.contains_key('key3'))

    def test_contains_key_example_2(self):
        m = HashMap(79, hash_function_2)
        keys = [i for i in range(1, 1000, 20)]
        for key in keys:
            m.put(str(key), key * 42)
        self.assertEqual(m.get_size(), len(keys))
        self.assertEqual(m.get_capacity(), 79)
        for key in keys:
            self.assertTrue(m.contains_key(str(key)))
            self.assertFalse(m.contains_key(str(key + 1)))

    def test_remove_example_1(self):
        m = HashMap(53, hash_function_1)
        self.assertIsNone(m.get('key1'))
        m.put('key1', 10)
        self.assertEqual(m.get('key1'), 10)
        m.remove('key1')
        self.assertIsNone(m.get('key1'))
        with self.assertRaises(KeyError):
            m.remove('key4')

    def test_get_keys_and_values_example_1(self):
        m = HashMap(11, hash_function_2)
        for i in range(1, 6):
            m.put(str(i), str(i * 10))
        self.assertEqual(m.get_keys_and_values(), DynamicArray([("1", "10"), ("2", "20"), ("3", "30"), ("4", "40"), ("5", "50")]))
        m.put('20', '200')
        m.remove('1')
        m.resize_table(2)
        self.assertEqual(m.get_keys_and_values(), DynamicArray([("2", "20"), ("3", "30"), ("4", "40"), ("5", "50"), ("20", "200")]))

    def test_clear_example_1(self):
        m = HashMap(101, hash_function_1)
        self.assertEqual(m.get_size(), 0)
        self.assertEqual(m.get_capacity(), 101)
        m.put('key1', 10)
        m.put('key2', 20)
        m.put('key1', 30)
        self.assertEqual(m.get_size(), 2)
        self.assertEqual(m.get_capacity(), 101)
        m.clear()
        self.assertEqual(m.get_size(), 0)
        self.assertEqual(m.get_capacity(), 101)

    def test_clear_example_2(self):
        m = HashMap(53, hash_function_1)
        self.assertEqual(m.get_size(), 0)
        self.assertEqual(m.get_capacity(), 53)
        m.put('key1', 10)
        self.assertEqual(m.get_size(), 1)
        self.assertEqual(m.get_capacity(), 53)
        m.put('key2', 20)
        self.assertEqual(m.get_size(), 2)
        self.assertEqual(m.get_capacity(), 53)
        m.resize_table(100)
        self.assertEqual(m.get_size(), 2)
        self.assertEqual(m.get_capacity(), 100)
        m.clear()
        self.assertEqual(m.get_size(), 0)
        self.assertEqual(m.get_capacity(), 100)   

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
        test_cases = [
            "test_put_example_1",
            "test_put_example_2",
            "test_resize_example_1",
            "test_resize_example_2",
            "test_table_load_example_1",
            "test_table_load_example_2",
            "test_empty_buckets_example_1",
            "test_empty_buckets_example_2",
            "test_get_example_1",
            "test_get_example_2",
            "test_contains_key_example_1",
            "test_contains_key_example_2",
            "test_remove_example_1",
            "test_get_keys_and_values_example_1",
            "test_clear_example_1",
            "test_clear_example_2",
            "test_find_mode_example_1",
            "test_find_mode_example_2"
        ]
        for test_case in test_cases:
            suite.addTest(TestHashMapSC(test_case))
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