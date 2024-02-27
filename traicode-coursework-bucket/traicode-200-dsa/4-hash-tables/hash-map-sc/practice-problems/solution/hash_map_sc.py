class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
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
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

# ------------------------------------------------------------------ #

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

