#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 20:46:08 2016

@author: abhibhat
"""
import logging
LOGGER = None


class BinaryTreeExp(Exception):
    pass


class BinaryTree(object):
    def __init__(self, arr, depth, no_of_queries):
        self.arr = arr
        self.depth = depth
        self.no_of_queries = no_of_queries
        self.value_index = dict()
        for index, elem in enumerate(arr):
            if elem > -1:
                self.value_index[elem] = index
        self.op_sum = []
        self.op = [{'sum': [], 'que': None} for _ in range(no_of_queries)]
        self.qry_index = 0
        LOGGER.debug("__init__: self.value_index = %s", self.value_index)

    def __iadd__(self, op):
        query, args = op.split(None, 1)
        LOGGER.debug("__iadd__(%s)", op)
        if query == 'SUM':
            x, y = map(int, args.split())
            if x >= 0:
                self.op[x]['sum'].append(lambda: self.Sum(y))
                LOGGER.debug("__iadd__: self.op[%s]['sum'] = %s",
                             x,
                             self.op[x]['sum'][-1])
            self.op_sum.append((x, y))
        else:
            fn = getattr(self, query.title())
            self.qry_index += 1
            self.op[self.qry_index]['que'] = lambda: fn(*args.split())
            LOGGER.debug("__iadd__: self.op[%s]['que'] = %s(%s), %s",
                         self.qry_index,
                         query,
                         args,
                         self.op[self.qry_index]['que'])
        return self

    def __call__(self):
        del self.op[self.qry_index + 1:]
        LOGGER.debug("__call__: self.op = %s", self.op)
        for index in range(len(self.op)):
            LOGGER.debug("__call__: self.op[%s] = %s", index, self.op[index])
            if self.op[index]['que']:
                try:
                    self.op[index]['que']()
                except IndexError:
                    self.depth += 1
                    extra_space = 2 ** (self.depth-1) - 2 ** self.depth
                    self.arr = self.arr + [-1] * extra_space
                    self.op[index]['que']()
            if self.op[index]['sum']:
                for si in range(len(self.op[index]['sum'])):
                    try:
                        self.op[index]['sum'][si] = self.op[index]['sum'][si]()
                    except KeyError as ex:
                        emsg = "Invalid Query, Node {} is absent".format(ex.message)
                        raise BinaryTreeExp(emsg)
            LOGGER.debug("__call__: self.op[[%s] = %s", index, self.op[index])
        return self

    def __iter__(self):
        for index, root in self.op_sum:
            LOGGER.debug("__iter__(%s, %s)", index, root)
            if index == -1:
                yield self.Sum(root)
            else:
                yield self.op[index]['sum'].pop(0)

    def Update(self, x, y):
        """UPDATE x y: Change the node with value x to y"""
        x, y = map(int, (x, y))
        index = self.value_index[x]
        LOGGER.debug("Update: index = %s", index)
        LOGGER.debug("Update: arr = %s", arr)
        self.arr[index] = y
        self.value_index[y] = index
        del self.value_index[x]
        LOGGER.debug("Update: value_index = %s", self.value_index)
        LOGGER.debug("Update: arr = %s", arr)

    def Add(self, x, y, z):
        """ADD x y z: Add a new node with a value z as y child of x. y is
        either "L" or "R". L represents Left child and R represents
        Right child."""
        x, z = map(int, (x, z))
        index = self.value_index[x]
        LOGGER.debug("Add: index = %s", index)
        if y == 'L':
            self.arr[2*index + 1] = z
            self.value_index[z] = 2*index
        elif y == 'R':
            self.arr[2*index + 2] = z
            self.value_index[z] = 2*index + 1
        LOGGER.debug("Add: value_index = %s", self.value_index)
        LOGGER.debug("Add: arr = %s", arr)

    def _has_left_child(self, index):
        return 2*index + 1 < len(arr) and arr[2*index + 1] != -1

    def _has_right_child(self, index):
        return 2*index + 2 < len(arr) and arr[2*index + 2] != -1

    def _is_leaf(self, index):
        return arr[index] == -1 or not self._has_left_child(index)

    def _last_child(self, index):
        LOGGER.debug("_last_child: self.arr[%s] = %s ",
                     index,
                     self.arr[index])
        debugMsg = "_recur_delete: _has_left_child = %s, _has_right_child = %s"
        LOGGER.debug(debugMsg,
                     self._has_left_child(index),
                     self._has_right_child(index))
        if self._has_right_child(index):
            return self._last_child(2*index + 2)
        elif self._has_left_child(index):
            return self._last_child(2*index + 1)
        else:
            return index

    def Delete(self, x):
        '''DELETE x: Delete the node with value x
        As the delete process was un-obvious, I replaced the last node from the
        subtree in the position of the current deleted node
        '''
        x = int(x)
        index = self.value_index[x]
        LOGGER.debug("Delete: index = %s", index)
        LOGGER.debug("Delete: arr = %s", arr)
        del self.value_index[self.arr[index]]
        last_child_index = self._last_child(index)
        LOGGER.debug("Delete: last_child_index = %s, self.arr[%s]",
                     last_child_index,
                     self.arr[last_child_index])
        self.arr[index] = self.arr[last_child_index]
        self.arr[last_child_index] = -1
        LOGGER.debug("Delete: value_index = %s", self.value_index)
        LOGGER.debug("Delete: arr = %s", arr)

    def _recur_sum(self, index):
        """Recursively compute the sum of the node values of the subtree rooted
        at index"""
        LOGGER.debug("_recur_sum: index = %s", index)
        if index >= len(self.arr) or self.arr[index] == -1:
            return 0
        LOGGER.debug("_recur_sum: self.arr[index] = %s", self.arr[index])
        return (self.arr[index] +
                self._recur_sum(2*index + 1) +
                self._recur_sum(2*index + 2))

    def Sum(self, y):
        """SUM x y: Output the sum of sub-tree rooted at y at state x.
        Initial state of the binary tree is 0. Each of the queries ADD, UPDATE
        or DELETE changes the state of the tree and the new state identifier
        will be one more than the previous state."""
        y = int(y)
        index = self.value_index[y]
        LOGGER.debug("Sum: index = %s", index)
        LOGGER.debug("Sum: value_index = %s", self.value_index)
        LOGGER.debug("Sum: arr = %s", arr)
        _sum = self._recur_sum(index)
        LOGGER.debug("Sum:  %s", _sum)
        return _sum


def set_logger(level=logging.WARNING):
    import os
    logger = logging.getLogger(os.path.basename(__file__))
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

LOGGER = set_logger(logging.WARNING)
depth = input()
arr = map(int, raw_input().split())
n = input()
bt = BinaryTree(arr, depth, n)
LOGGER.debug("ADD = %s", bt.Add)
LOGGER.debug("UPDATE = %s", bt.Update)
LOGGER.debug("DEBUG = %s", bt.Delete)
LOGGER.debug("SUM = %s", bt.Sum)
for _ in range(n):
    qry = raw_input()
    bt += qry

for result in bt():
    print result
