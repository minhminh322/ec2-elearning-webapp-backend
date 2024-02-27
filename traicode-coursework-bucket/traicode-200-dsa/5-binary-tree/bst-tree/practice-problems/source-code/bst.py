class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

#------------------------***YOUR IMPLEMENTATION***------------------------#

    def add(self, value: object) -> None:
        """
        TODO: Write your implementation
        """
        pass

    def remove(self, value: object) -> bool:
        """
        TODO: Write your implementation
        """
        pass

    def contains(self, value: object) -> bool:
        """
        TODO: Write your implementation
        """
        pass

    def inorder_traversal(self) -> Queue:
        """
        TODO: Write your implementation
        """
        pass

    def find_min(self) -> object:
        """
        TODO: Write your implementation
        """
        pass

    def find_max(self) -> object:
        """
        TODO: Write your implementation
        """
        pass

    def is_empty(self) -> bool:
        """
        TODO: Write your implementation
        """
        pass

    def make_empty(self) -> None:
        """
        TODO: Write your implementation
        """
        pass
