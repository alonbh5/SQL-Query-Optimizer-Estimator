# CLASSES
from enum import Enum


class Type(Enum):
    PI = "PI"
    SIGMA = "SIGMA"
    CARTESIAN = "CARTESIAN"
    NJOIN = "NJOIN"

    def print(self):
        print(self.value, end="")


class Schema:
    def __init__(self, i_name: str):
        self.name = i_name
        self.table: list = []
        self.col_list: list = []
        self.n_Size = None
        self.R_size = None
        self.iter = None

    def insertTable(self, table):
        self.table.append(table)

    def insertCol(self, col, size):
        fullCol = self.name + "." + col
        self.col_list.append(Col(fullCol, size))

    def insertNumOfRows(self, size):
        self.n_Size = size

    def indsertRowSize(self, size):
        self.R_size = size

    def getValueOfCol(self, col):
        for i in self.col_list:
            if i.name == col:
                return i.value

    def printSchema(self, cond: str):
        if cond == "Output" or cond == "Input":
            print(cond, end=" ")
        x = 4
        print("n_Scheme" + str(self.iter) + "=" + str(self.n_Size) + " R_Scheme" + str(self.iter) + "=" + str(self.R_size))


class Col:
    def __init__(self, i_name, i_size):
        self.name = i_name
        self.value = i_size



def printNJOINORCARTESIANValue(node):
    if type(node) is Node:
        node.printCurrNode()
        if type(node.next) is Node:
            print("(", end="")
            node.next.printCurrNode()
            print(")", end="")
        if node.left is not None:
            print("("+node.left+")", end="")
        elif node.right is not None:
            print("("+node.right+")", end="")

    elif node is not None:
        print(node, end="")



class Node:
    def __init__(self, i_type, i_value):
        self.type = i_type
        self.value = i_value
        self.left = None
        self.right = None
        if self.type == Type.CARTESIAN:
            idx = i_value.find(",")
            if idx != -1:
                self.left = i_value[0:idx].strip()
                self.right = i_value[idx+1:].strip()
        self.next = None
        self.prev = None


    def insertInside(self, newNode):
        if self.next is not None:
            newNode.next = self.next
            newNode.prev = self
            self.next = newNode
            newNode.next.prev = newNode
        else:
            self.next = newNode
            newNode.prev = self


    def printList(self):
        self.printCurrNode()
        if self.next is not None:
            print("(", end="")
            self.next.printList()
            print(")", end="")

    def printCurrNode(self):

        if self.type == Type.CARTESIAN and self.value.find(",") == -1: #case its CARTESIAN with only one table print only (R)/(S)
            print("("+self.value+")",end="")
        else:
            self.type.print()
            bracket = ["[", "]"]
            if self.type is Type.CARTESIAN or self.type is Type.NJOIN:
                bracket[0] = OPEN_BRACKET
                bracket[1] = CLOSE_BRACKET
            print(bracket[0], end="")
            if self.type is Type.NJOIN or self.type is Type.CARTESIAN:
                if self.left is None and self.right is None:
                    print(self.value, end="")
                else:
                    printNJOINORCARTESIANValue(self.left)
                    print(",", end="")
                    printNJOINORCARTESIANValue(self.right)
            else:
                print(self.value, end="")
            print(bracket[1], end="")




class SLinkedList:
    def __init__(self):
        self.head = None

    def print(self):
        currentNode = self.head
        if currentNode is not None:
            currentNode.printList()
        print()

    def insertAfter(self, node_before, newNode):
        if node_before is None:  # insert to head
            self.head = newNode
        else:
            temp = node_before.next
            node_before.next = newNode
            newNode.next = temp


R_COL = ["R.A", "R.B", "R.C", "R.D", "R.E"]
S_COL = ["S.D", "S.E", "S.F", "S.H", "S.I"]
AND_EXPRESSION = " AND "
OR_EXPRESSION = " OR "
INDEX_RULE_4 = 0
OPEN_BRACKET = "("
CLOSE_BRACKET = ")"
MULTIPLY_SIGN = "*"
PLUS_SIGN = "+"
EQUAL_SIGN = "="
COMMA_SIGN = ","
BOUNDARY_LINE = "-------------------------------"
Schema_Iteration = 0
list_of_queries: list = []
WHITESPACE = " "
EMPTY = ""
Schema_R = Schema("R")
Schema_S = Schema("S")
SchemaIO = Schema("IO")

