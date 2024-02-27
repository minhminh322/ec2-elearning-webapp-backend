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
    
class HashMapSolution:
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

    def put(self, key: str, value: object) -> None:
        if self.table_load() >= 1:
            new_capacity = self.get_capacity() * 2
            self.resize_table(new_capacity)
        
        hash_key = self._hash_function(key) % self._capacity 
        bucket = self._buckets[hash_key]

        for node in bucket:
            if node.key == key:
                node.value = value
                return
        bucket.insert(key, value)
        self._size += 1
        
    def resize_table(self, new_capacity: int) -> None:
        if new_capacity < 1:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        new_table = HashMap(new_capacity, self._hash_function)
        for index in range(self._capacity):
            bucket = self._buckets.get_at_index(index)
            for node in bucket:
                new_table.put(node.key, node.value)

        self._buckets = new_table._buckets
        self._size = new_table._size
        self._capacity = new_table._capacity

    def table_load(self) -> float:
        load_factor = float(self.get_size() / self.get_capacity())
        return load_factor 

    def empty_buckets(self) -> int:
        num_of_empty = 0
        for index in range(self._capacity):
            bucket = self._buckets.get_at_index(index)
            if bucket.length() == 0:
                num_of_empty += 1
        return num_of_empty 

    def get(self, key: str):
        find_hash_key = self._hash_function(key) % self._capacity
        bucket = self._buckets[find_hash_key]

        for node in bucket:
            if node.key == key:
                return node.value
        return None

    def contains_key(self, key: str) -> bool:
        find_hash_key = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(find_hash_key)

        for node in bucket:
            if node.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        find_hash_key = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(find_hash_key)

        node = bucket.contains(key)
        if node:
            bucket.remove(key)
            self._size -= 1
            return None


    def get_keys_and_values(self) -> DynamicArray:
        results_array = DynamicArray()
        for i in range(self._capacity):
            for node in self._buckets[i]:
                results_array.append((node.key, node.value))
        return results_array


    def clear(self) -> None:
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()
        self._size = 0

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

    def put(self, key: str, value: object) -> None:
        if self.table_load() >= 1:
            new_capacity = self.get_capacity() * 2
            self.resize_table(new_capacity)
        
        hash_key = self._hash_function(key) % self._capacity 
        bucket = self._buckets[hash_key]

        for node in bucket:
            if node.key == key:
                node.value = value
                return
        bucket.insert(key, value)
        self._size += 1
        
    def resize_table(self, new_capacity: int) -> None:
        if new_capacity < 1:
            return

        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        new_table = HashMap(new_capacity, self._hash_function)
        for index in range(self._capacity):
            bucket = self._buckets.get_at_index(index)
            for node in bucket:
                new_table.put(node.key, node.value)

        self._buckets = new_table._buckets
        self._size = new_table._size
        self._capacity = new_table._capacity

    def table_load(self) -> float:
        load_factor = float(self.get_size() / self.get_capacity())
        return load_factor 

    def empty_buckets(self) -> int:
        num_of_empty = 0
        for index in range(self._capacity):
            bucket = self._buckets.get_at_index(index)
            if bucket.length() == 0:
                num_of_empty += 1
        return num_of_empty 

    def get(self, key: str):
        find_hash_key = self._hash_function(key) % self._capacity
        bucket = self._buckets[find_hash_key]

        for node in bucket:
            if node.key == key:
                return node.value
        return None

    def contains_key(self, key: str) -> bool:
        find_hash_key = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(find_hash_key)

        for node in bucket:
            if node.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        find_hash_key = self._hash_function(key) % self._capacity
        bucket = self._buckets.get_at_index(find_hash_key)

        node = bucket.contains(key)
        if node:
            bucket.remove(key)
            self._size -= 1
            return None


    def get_keys_and_values(self) -> DynamicArray:
        results_array = DynamicArray()
        for i in range(self._capacity):
            for node in self._buckets[i]:
                results_array.append((node.key, node.value))
        return results_array


    def clear(self) -> None:
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()
        self._size = 0


# --------------------------UNIT TESTS------------------------------------
class TestHashMapSC(unittest.TestCase):
    def test_put_and_get(self):
        hash_map = HashMap()
        hash_map.put("apple", 5)
        self.assertEqual(hash_map.get("apple"), 5)
        
    def test_put_and_load_factor(self):
        m = HashMap(101, hash_function_1)
        m_sol = HashMapSolution(101, hash_function_1)
        self.assertAlmostEqual(m.table_load(), m_sol.table_load(), delta=0.01)
        m.put('key1', 10)
        m_sol.put('key1', 10)
        self.assertAlmostEqual(m.table_load(), m_sol.table_load(), delta=0.01)
        m.put('key2', 20)
        m_sol.put('key2', 20)
        self.assertAlmostEqual(m.table_load(), m_sol.table_load(), delta=0.01)
        m.put('key1', 30)
        m_sol.put('key1', 30)
        self.assertAlmostEqual(m.table_load(), m_sol.table_load(), delta=0.01)

    def test_put_and_resize_table(self):
        m = HashMap(20, hash_function_1)
        m_sol = HashMapSolution(20, hash_function_1)

        m.put('key1', 10)
        m_sol.put('key1', 10)
        self.assertEqual(m.get_size(), m_sol.get_size())
        self.assertEqual(m.get_capacity(), m_sol.get_capacity())
        self.assertEqual(m.get('key1'), m_sol.get('key1'))

        m.resize_table(30)
        m_sol.resize_table(30)
        self.assertEqual(m.get_size(), m_sol.get_size())
        self.assertEqual(m.get_capacity(), m_sol.get_capacity())
        self.assertEqual(m.get('key1'), m_sol.get('key1'))

    def test_remove(self):
        hash_map = HashMap()
        hash_map.put("apple", 5)
        hash_map.put("banana", 7)
        hash_map.remove("apple")
        self.assertIsNone(hash_map.get("apple"))
        self.assertIsNotNone(hash_map.get("banana"))

    def test_clear(self):
        hash_map = HashMap()
        hash_map.put("apple", 5)
        hash_map.put("banana", 7)
        self.assertEqual(hash_map.get_size(), 2) 
        hash_map.clear()
        self.assertIsNone(hash_map.get("apple")) 
        self.assertEqual(hash_map.get_size(), 0) 

    def test_contains_key(self):
        hash_map = HashMap()
        hash_map.put("apple", 5)
        self.assertTrue(hash_map.contains_key("apple"))
        self.assertFalse(hash_map.contains_key("banana"))
        
    def test_empty_buckets(self):
        hash_map = HashMap()
        hash_map.put("apple", 5)
        self.assertEqual(hash_map.empty_buckets(), hash_map.get_capacity() - 1)
        
    def test_get_keys_and_values(self):
        hash_map = HashMap()
        hash_map.put("apple", 5)
        hash_map.put("banana", 7)
        hash_map.put("orange", 3)
        result = hash_map.get_keys_and_values()
        expected = [("apple", 5), ("banana", 7), ("orange", 3)]
        self.assertEqual(str(result), str(expected))

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
        test_cases = ["test_put_and_get", "test_put_and_load_factor", "test_put_and_resize_table", "test_remove", "test_clear", "test_contains_key", "test_empty_buckets", "test_get_keys_and_values"]
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
