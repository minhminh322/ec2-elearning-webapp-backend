class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity) # From static_array.py

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        """
        return self._capacity

#------------------------***YOUR IMPLEMENTATION***------------------------#

    def resize(self, new_capacity: int) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def append(self, value: object) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def insert_at_index(self, index: int, value: object) -> None:
        """
        TODO: Write this implementation
        """
        pass

    def remove_at_index(self, index: int) -> None:
        """
        TODO: Write this implementation
        """
        pass

