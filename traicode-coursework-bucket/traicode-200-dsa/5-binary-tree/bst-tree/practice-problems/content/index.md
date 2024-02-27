# Implementing a Binary Search Tree (BST)

Implement a Binary Search Tree (BST) class.

## Provided Classes

RESTRICTIONS: You are NOT allowed to use ANY built-in Python data structures and/or their methods. In case you need ‘helper’ data structures in your solution, the skeleton code includes prewritten implementations of Queue and Stack classes. You are allowed to create and use objects from those classes in your implementation.

## Implementation

Your task is to implement the following methods in the BST class:

1. `add(self, value: object) -> None`: Adds a new node with the given value to the tree. Duplicate values are allowed. If a node with that value is already in the tree, the new value should be added to the right subtree of that node. It must be implemented with O(N) runtime complexity.

2. `remove(self, value: object) -> bool`: This method removes a value from the tree. The method returns True if the value is removed. Otherwise, it returns False. It must be implemented with O(N) runtime complexity.
   When removing a node with two subtrees, replace it with the leftmost child of the right subtree (i.e. the inorder successor). You do not need to recursively continue this process. If the deleted node only has one subtree (either right or left), replace the deleted node with the root node of that subtree.

3. `contains(self, value: object) -> bool`: This method returns True if the value is in the tree. Otherwise, it returns False. If the tree is empty, the method should return False. It must be implemented with O(N) runtime complexity.

4. `in_order_traversal(self) -> Queue`: This method will perform an inorder traversal of the tree and return a Queue object that contains the values of the visited nodes, in the order they were visited. If the tree is empty, the method returns an empty Queue. It must be implemented with O(N) runtime complexity.

5. `find_min(self) -> object`: This method returns the minimum value in the tree. If the tree is empty, the method should return None. It must be implemented with O(N) runtime complexity.

6. `find_max(self) -> object`: This method returns the maximum value in the tree. If the tree is empty, the method should return None. It must be implemented with O(N) runtime complexity.

7. `is_empty(self) -> bool`: This method returns True if the tree is empty. Otherwise, it returns False. It must be implemented with O(1) runtime complexity.

8. `make_empty(self) -> None`: This method removes all nodes from the tree. It must be implemented with O(1) runtime complexity.
