# Implementing a Hash Map with Separate Chaining

Implement a hash map using separate chaining. The hash map should use a dynamic array to store the hash table and linked lists to store chains of key/value pairs.

## Separate Chaining

Separate Chaining is one of the techniques that is used to resolve the collision. This method combines a linked list with a hash table in order to resolve the collision. When two or more elements are hash to the same location, these elements are represented into a singly-linked list like a chain.

In separate chaining, each slot of the hash table is a linked list. We will insert the element into a specific linked list to store it in the hash table. If there is any collision i.e. if more than one element after calculating the hashed value mapped to the same key then we will store those elements in the same linked list.

## Load Factor

The load factor is a measure of how full the hash table is allowed to get before its capacity is automatically increased. The load factor is used to decide when to increase the capacity of the hash table.

Load Factor = Total elements in hash table / Size of hash table

## Provided Classes

Two pre-written classes are provided for you in the skeleton code - DynamicArray and LinkedList. You must use objects of these classes in your HashMap class implementation. Use a DynamicArray object to store your hash table, and LinkedList objects to store chains of key/value pairs.

RESTRICTIONS: You are NOT allowed to use ANY built-in Python data structures and/or their methods.

## Implementation

Your task is to implement the following methods in the HashMap class:

1. `put(key: string, value: object) -> None`: This method updates the key/value pair in the hash map. If the given key already exists in the hash map, its associated value must be replaced with the new value. If the given key is not in the hash map, a new key/value pair must be added.
**For this hash map implementation, the table must be resized to double its current capacity when this method is called and the current load factor of the table is greater than or equal to 1.0.**

2. `empty_buckets() -> int`: This method returns the number of empty buckets in the hash table.

3. `table_load() -> float`: This method returns the current load factor of the hash table.

4. `clear() -> None`: This method clears the contents of the hash map. It does not change the underlying hash table capacity.

5. `resize_table(new_capacity: int) -> None`: This method changes the capacity of the internal hash table. All existing key/value pairs must remain in the new hash map, and all hash table links must be rehashed. (Consider calling another HashMap method for this part). First check that new_capacity is not less than 1; if so, the method does nothing. If new_capacity is 1 or more, make sure it is a prime number. If not, change it to the next highest prime number. You may use the methods \_is_prime() and \_next_prime() from the skeleton code.

6. `get(key: string) -> object`: This method returns the value associated with the given key, or None if the key is not in the hash map.

7. `contains_key(key: string) -> bool`: This method returns True if the given key is in the hash map, and False otherwise. An empty hash map does not contain any keys.

8. `remove(key: string) -> None`: This method removes the key and its associated value from the hash map. If the key is not in the hash map, the method does nothing.

9. `get_keys_and_values() -> DynamicArray`: This method returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map. The order of the keys in the dynamic array does not matter.

## Example:

```plaintext
hash_map = HashMap()
hash_map.put("a", 1)
hash_map.put("b", 2)
hash_map.get("a") ➞ 1
hash_map.get("b") ➞ 2
hash_map.table_load() ➞ 0.2
hash_map.put("c", 3)
hash_map.table_load() ➞ 0.3
hash_map.remove("a")
hash_map.contains_key("a") ➞ False
hash_map.get_keys_and_values() ➞ [("b", 2), ("c", 3)]
hash_map.clear()
hash_map.get_keys_and_values() ➞ []
```
