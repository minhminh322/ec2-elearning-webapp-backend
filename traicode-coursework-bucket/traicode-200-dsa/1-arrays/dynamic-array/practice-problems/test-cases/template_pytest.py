import pytest
import sys

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

# --------------------------REPLACE CODE----------------------------------

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

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        if new_capacity > 0 and new_capacity >= self._size:
            self._capacity = new_capacity 

            temp = StaticArray(self._capacity)

            for index in range(self._size):
                temp[index] = self._data[index]

            self._data = temp

    def append(self, value: object) -> None:
        if self._size == self._capacity:
            self.resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        if index < 0 or index > self._size:
            raise DynamicArrayException
        if self._capacity == self._size:
            self.resize(self._capacity * 2)
        
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i-1]
    
        self._data[index] = value
        # print("Hallo")
        self._size += 1

    def remove_at_index(self, index: int) -> None:
        if index < 0 or index > self._size - 1:
            raise DynamicArrayException
        print("TEST Remove sample 000")
        if self._capacity > 10 and self._size < self._capacity / 4:
            resize_capacity = self._size * 2
            if resize_capacity < 10:
                resize_capacity = 10
            
            self.resize(resize_capacity)

        print("TEST Remove sample")
        for i in range(index + 1, self._size):
            self._data[i - 1] = self._data[i]
        self._size -= 1


class TestDynamicArray:
    def test_empty_dynamic_array(self):
        arr = DynamicArray()
        assert arr.is_empty()
        assert arr.length() == 0
        assert arr.get_capacity() == 4

    def test_dynamic_array_with_initial_values(self):
        arr = DynamicArray([1, 2, 3, 4])
        assert not arr.is_empty()
        assert arr.length() == 4
        assert arr.get_capacity() == 4

    def test_append(self):
        arr = DynamicArray()
        arr.append(1)
        arr.append(2)
        assert arr.length() == 2
        assert arr.get_capacity() == 4
        assert arr[0] == 1
        assert arr[1] == 2

    def test_insert_at_index(self):
        arr = DynamicArray([1, 2, 4, 5])
        arr.insert_at_index(2, 3)
        assert arr.length() == 5
        assert arr[2] == 3
        assert arr[3] == 4

    def test_remove_at_index(self, capsys):
        arr = DynamicArray([1, 2, 3, 4, 5])
        arr.remove_at_index(2)
        assert arr.length() == 4
        assert arr[2] == 4
        out, err = capsys.readouterr()
        print("Hi ",out, err)
        with pytest.raises(DynamicArrayException):
            arr.remove_at_index(10)  # Trying to remove an out-of-bound index should raise an exception


if __name__ == "__main__":
    # Run the unit tests
    pytest.main(["-v", "template_pytest.py"])