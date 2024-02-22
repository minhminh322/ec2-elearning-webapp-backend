class DynamicArray:
    """
    Class implementing a Dynamic Array
    Supported methods are:
    append, pop, swap, get_at_index, set_at_index, length
    """

    def __init__(self, arr=None) -> None:
        """Initialize new dynamic array using a list."""
        self._data = arr.copy() if arr else []

    def __iter__(self):
        """
        Disable iterator capability for DynamicArray class
        This means loops and aggregate functions like
        those shown below won't work:

        da = DynamicArray()
        for value in da:        # will not work
        min(da)                 # will not work
        max(da)                 # will not work
        sort(da)                # will not work
        """
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
