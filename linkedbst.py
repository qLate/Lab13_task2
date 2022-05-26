"""
File: linkedbst.py
Author: Ken Lambert
"""
import random
from math import ceil
from math import log

from abstractcollection import AbstractCollection
from linkedstack import LinkedStack


class BSTNode(object):
    """Represents a node for a linked binary search tree."""

    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def is_leaf(self):
        """ checks if leaf node"""
        return self.left is None and self.right is None


class LinkedBST(AbstractCollection):
    """A link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if item not in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while current_node.right is not None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while current_node is not None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if current_node.left is not None \
                and current_node.right is not None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        """

        def height1(top):
            """
            Helper function
            """
            if top is None:
                return 0
            if top.is_leaf():
                return 0

            return 1 + max(height1(top.left), height1(top.right))

        return height1(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        """

        return self.height() < 2 * log(self._size + 1, 2) - 1

    def range_find(self, low, high):
        """
        Returns a list of the items in the tree, where low <= item <= high.
        """
        lst = []

        def recurse(node):
            if node is None:
                return

            if high < node.data:
                recurse(node.left)
                return
            elif low > node.data:
                recurse(node.right)
                return

            lst.append(node.data)
            recurse(node.left)
            recurse(node.right)

        recurse(self._root)
        return lst if len(lst) != 0 else None

    def rebalance(self):
        """
        Rebalances the tree.
        """

        lst = list(self.inorder())
        lst.sort()

        self.clear()

        def add_middle(lst):
            if len(lst) == 0:
                return
            self.add(lst.pop(len(lst) // 2))

            mid = ceil(len(lst) / 2)
            add_middle(lst[:mid])
            add_middle(lst[mid:])

        add_middle(lst)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        """

        def recurse(node, prev):
            if node is None:
                return prev
            elif node.data <= item:
                if prev is not None and prev > item:
                    return prev
                else:
                    return recurse(node.right, node.data)
            elif node.data > item:
                return recurse(node.left, node.data)

        return recurse(self._root, None)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        """

        def recurse(node, prev):
            if node is None:
                return prev
            elif node.data >= item:
                if prev is not None and prev < item:
                    return prev
                else:
                    return recurse(node.left, node.data)
            elif node.data < item:
                return recurse(node.right, node.data)

        return recurse(self._root, None)

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        """

        with open(path, 'r', encoding='utf-8') as file:
            items = [word.strip() for word in file.readlines()]
            for item in items:
                self.add(item)

        for _ in range(10000):
            self.find(random.choice(items))


import sys

sys.setrecursionlimit(100000)

if __name__ == "__main__":
    lbst = LinkedBST()
    # lbst.add(1)
    # lbst.add(2)
    # lbst.add(3)
    # lbst.add(4)
    # lbst.add(5)
    # lbst.add(6)
    # lbst.add(7)
    #
    # lbst.rebalance()
    # print(lbst.is_balanced())

    lbst.demo_bst("words.txt")
