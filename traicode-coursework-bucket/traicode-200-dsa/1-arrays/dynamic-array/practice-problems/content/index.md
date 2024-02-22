# Starter Code

- You will be provided with a starter “skeleton” code, on which you will build your implementation. Methods defined in the skeleton code must retain their names and input/output parameters. Variables defined in the skeleton code must also retain their names. We will only test your solution by making calls to methods defined in the skeleton code, and by checking values of variables defined in the skeleton code.

## **Specific Instructions**

There are 10 separate problems in this assignment. For each problem, you will write a Python function according to the provided specifications. The skeleton code and some basic test cases for each problem are provided in the exercise.

Most problems will take as input (and sometimes return as output) an object of the StaticArray class. The **StaticArray** class has been pre-written for you, and is located in the file _static_array.py_

**StaticArray** is a very simple class that simulates the behavior of a fixed size array. It has only four methods, and contains code to support bracketed indexing ([]):

> init() - Creates a new static array that will store a fixed number of elements. Once the StaticArray is created, its size cannot be changed.
> set() - Changes the value of any element using its index.
> get() - Reads the value of any element using its index.
> length() - Queries the number of elements in the array.

Please review the code and comments in the StaticArray class to better understand the available methods, their use, and input/output parameters. Note that since StaticArray is intentionally a very simple class, it does not possess the many capabilities typically associated with Python lists. You need to write your solutions using only the available StaticArray functionality, as described above.

### **RESTRICTIONS:**

You are NOT allowed to use ANY built-in Python data structures and/or their methods in any of your solutions. This includes built-in Python lists, dictionaries, or anything else. Variables for holding a single value, or a tuple holding at most three values, are allowed. It is also OK to use range().

You are NOT allowed to directly access any variables of the StaticArray class (e.g. _self.\_size_ or _self.\_data_). Access to StaticArray variables must be done by using the StaticArray class methods.
