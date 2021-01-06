from classes import *
from random import randrange
import copy
import math

# *** General - Auxilary - get random rule (4/4a/5/6/6a/11b) ***#
def rand_rule():
    rnd = randrange(0, 6)
    x = -1
    if rnd == 0:
        x = "4"
    if rnd == 1:
        x = "4a"
    if rnd == 2:
        x = "5a"
    if rnd == 3:
        x = "6"
    if rnd == 4:
        x = "6a"
    if rnd == 5:
        x = "11b"
    return x


# *** Part Three - Auxilary - calculate probability of val in col - 1/V(X) ***#
def get_probability_of_val_appearance(col: str, table: str):
    if table == "S":
        result = "1/" + str(Schema_S.getValueOfCol(col))
    if table == "R":
        result = "1/" + str(Schema_R.getValueOfCol(col))
    return result

# *** Part Three - Auxilary - calculate probability of colA = Col.B ***#
def handel_cols_values(col1, col2):
    if col1 == col2:
        return "1"
    if col1 in S_COL:
        n_val1 = Schema_S.getValueOfCol(col1)
    else:
        n_val1 = Schema_R.getValueOfCol(col1)
    if col2 in S_COL:
        n_val2 = Schema_S.getValueOfCol(col2)
    else:
        n_val2 = Schema_R.getValueOfCol(col2)
    return "1/" + str(max(int(n_val1), int(n_val2)))

# *** Part Three - Auxilary - calculate probability of colA = int val ***#
def handel_int_values(val1, val2):
    str_result = EMPTY
    if is_int(val1):
        if is_int(val2):
            if val1 == val2:
                str_result += str(1)
            else:
                str_result += str(0)
        else:
            if val2 in S_COL:
                str_result += get_probability_of_val_appearance(val2, "S")
            else:
                str_result += get_probability_of_val_appearance(val2, "R")
    else:
        return handel_int_values(val2, val1)
    return str_result



# *** Part Three - Auxilary - change all cols to probability val and return equation string  ***#
def change_col_to_probability_val(equation_list: list):
    equation_str = EMPTY
    for i in range(0,  len(equation_list)):
        val = equation_list[i]
        if val == OPEN_BRACKET or val == CLOSE_BRACKET or val == MULTIPLY_SIGN or val == PLUS_SIGN:
            equation_str += str(val)
        if val == EQUAL_SIGN:
            val1 = equation_list[i-1]
            val2 = equation_list[i+1]
            if is_int(val1) or is_int(val2):
                equation_str += handel_int_values(val1, val2)
            else:
                equation_str += handel_cols_values(val1, val2)
    return equation_str

# *** Part Three - Auxilary - get the equation str for NJOIN ***#
def getEquationNJOINstring():
    rows = Schema_S.n_Size * Schema_R.n_Size
    return str(rows) + MULTIPLY_SIGN + OPEN_BRACKET + handel_cols_values("R.E", "S.E") + MULTIPLY_SIGN +  handel_cols_values("R.D", "S.D") + CLOSE_BRACKET


# *** Part Three - Auxilary - calculate Schema after CARTESIAN/NJOIN and print I/O ***#
def calculte_print_njoin_or_cartesian(currNode: Node):
    global Schema_Iteration
    SchemOutput: Schema = Schema("IO")
    if type(currNode.left) is Node:
        run_input_output_data(currNode.left, Type.NJOIN)
        print(EMPTY)
    if type(currNode.right) is Node:
        run_input_output_data(currNode.right, Type.NJOIN)
        print(EMPTY)

    currNode.printCurrNode()
    print(EMPTY)
    print("input: n_R=" + str(Schema_R.n_Size) + " n_S=" + str(Schema_S.n_Size) + " R_R=" + str(
        Schema_R.R_size) + " R_S=" + str(Schema_S.R_size))
    Schema_Iteration = Schema_Iteration + 1
    SchemOutput.iter = Schema_Iteration
    if currNode.type == Type.NJOIN:
        SchemOutput.insertNumOfRows(math.ceil(eval(getEquationNJOINstring())))
    else:
        SchemOutput.insertNumOfRows(Schema_S.n_Size * Schema_R.n_Size)
    SchemOutput.indsertRowSize(Schema_S.R_size + Schema_R.R_size)
    SchemOutput.printSchema("Output")
    return SchemOutput


# *** Part Three - Auxilary - calculate Schema after PI and print I/O ***#
def calculte_print_pi(currNode: Node):
    global Schema_Iteration
    SchemOutput: Schema = Schema("IO")

    currNode.printCurrNode()
    print(EMPTY)
    SchemaIO.printSchema("Input")
    value_list = currNode.value.replace(",", " ").split()
    Schema_Iteration = Schema_Iteration + 1
    SchemOutput.iter = Schema_Iteration
    SchemOutput.insertNumOfRows(SchemaIO.n_Size)
    SchemOutput.indsertRowSize(len(value_list) * 4)
    SchemOutput.printSchema("Output")
    return SchemOutput


# *** Part Three - Auxilary - calculate Schema after SIGMA and print I/O ***#
def calculte_print_sigma(currNode: Node, type):
    global Schema_Iteration
    global Schema_R
    global Schema_S
    SchemOutput: Schema = Schema("IO")
    flag = False
    if type == Type.NJOIN or type == Type.CARTESIAN:
        flag = True
        if currNode.left == "R" or currNode.right == "R":
            schema_name = "R"
        else:
            schema_name = "S"

    currNode.printCurrNode()
    print(EMPTY)

    if flag and schema_name == "R":
        print("input: n_R=" + str(Schema_R.n_Size) + " R_R=" + str(Schema_R.R_size))
    elif flag and schema_name == "S":
        print("input: n_S= " + str(Schema_S.n_Size) + " S_R=" + str(Schema_S.R_size))
    else:
        SchemaIO.printSchema("Input")

    str_list = currNode.value.replace(AND_EXPRESSION, " * ").replace(OR_EXPRESSION, " + ").replace("=", " = ").replace(
        "(", " ( ").replace(")", " ) ").split()
    equation_str = change_col_to_probability_val(str_list)
    equation_str = OPEN_BRACKET + equation_str + CLOSE_BRACKET + MULTIPLY_SIGN
    Schema_Iteration = Schema_Iteration + 1

    if flag and schema_name == "R":
        equation_str += str(Schema_R.n_Size)
        Schema_R.insertNumOfRows(math.ceil(eval(equation_str)))
        print("output: n_R=" + str(Schema_R.n_Size) + " R_R=" + str(Schema_R.R_size))
        SchemOutput = Schema_R
    elif flag and schema_name == "S":
        equation_str += str(Schema_S.n_Size)
        Schema_S.insertNumOfRows(math.ceil(eval(equation_str)))
        print("output: n_S=" + str(Schema_S.n_Size) + " S_R=" + str(Schema_S.R_size))
        SchemOutput = Schema_S
    else:
        equation_str += str(SchemaIO.n_Size)
        SchemOutput.insertNumOfRows(math.ceil(eval(equation_str)))
        SchemOutput.indsertRowSize(SchemaIO.R_size)
        SchemOutput.iter = Schema_Iteration
        SchemOutput.printSchema("Output")
    return SchemOutput


# **** Function returns indexes of all the occurrences of a substring in a string ****#
def find_all(a_string, sub):
    result = []
    k = 0
    while k < len(a_string):
        k = a_string.find(sub, k)
        if k == -1:
            return result
        else:
            result.append(k)
            k += 1
    return result


##**** Function checks if value is int type ****#
def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


##**** Function checks if value is constant ****#
def is_constant(constant_str: str, tables):
    constant_str = constant_str.strip()
    res = is_int(constant_str) or constant_str in tables
    return res


##**** Function checks if value is simple condition ****#
def is_simple_condition(condition: str, tables: list):
    condition = condition.strip()

    if condition.find("=") == -1:
        return False

    op_start_index = condition.find("=")
    op_end_index = op_start_index + 1
    constant_1 = condition[0:op_start_index].strip()
    constant_2 = condition[op_end_index:].strip()
    return is_constant(constant_1, tables) and is_constant(constant_2, tables)


##**** Function gets tables from condition str ****#
def get_table_from_condition(condition: str, tables: list):
    list_arr = find_all("=")

    if condition.find("=") == -1:
        return False

    op_start_index = condition.find("=")
    op_end_index = op_start_index + 1
    constant_1 = condition[0:op_start_index].strip()
    constant_2 = condition[op_end_index:].strip()
    return is_constant(constant_1, tables) and is_constant(constant_2, tables)


# *** Function return end index of the expression (AND/OR) ***#
def get_end_index_expression(cond_query, start_index):
    if cond_query.startswith(AND_EXPRESSION):
        return start_index + len(AND_EXPRESSION)
    if cond_query.startswith(OR_EXPRESSION):
        return start_index + len(OR_EXPRESSION)
    return -1


##**** Function checks if value is condition ****#
def is_condition(user_query: str, table_list):
    user_query = user_query.strip()
    query_len = len(user_query)
    global INDEX_RULE_4

    if query_len > 2 and user_query[0] == OPEN_BRACKET and user_query[query_len - 1] == CLOSE_BRACKET:
        if is_condition(user_query[1:query_len - 1], table_list):
            INDEX_RULE_4 += 1
            return True
    # get list of start indexes of and expressions - AND|OR
    listOfIndexes = find_all(user_query, AND_EXPRESSION) + find_all(user_query, OR_EXPRESSION)

    for ex_start_index in listOfIndexes:
        ex_end_index = get_end_index_expression(user_query[ex_start_index:], ex_start_index)
        left_condition = user_query[0:ex_start_index]
        right_condition = user_query[ex_end_index:]
        if is_condition(left_condition, table_list) and is_condition(right_condition, table_list):
            INDEX_RULE_4 = ex_start_index
            return True

    flag = is_simple_condition(user_query, table_list)
    if not flag:
        INDEX_RULE_4 = 0
    return flag


##**** Function remove bad bruckets ****#
def remove_bad_brucket(str: str):
    if str[0] == OPEN_BRACKET and str[len(str) - 1] != CLOSE_BRACKET:
        str = str[1:]
    if str[0] != OPEN_BRACKET and str[len(str) - 1] == CLOSE_BRACKET:
        str = str[0:len(str) - 1]
    return str


##**** Function checks if two cols equal ****#
def is_colume_equal(l_cond: str, r_cond: str):
    idx_dot1 = l_cond.find(".")
    idx_dot2 = r_cond.find(".")
    if idx_dot1 == -1 or idx_dot2 == -1:
        return False
    col_l = l_cond[idx_dot1 + 1:]
    col_r = r_cond[idx_dot2 + 1:]
    if col_l == col_r:
        return True


##**** Find all appreances of sub string ****#
def find_all(a_string, sub):
    result = []
    k = 0
    while k < len(a_string):
        k = a_string.find(sub, k)
        if k == -1:
            return result
        else:
            result.append(k)
            k += 1
    return result


##**** Function prints menu ****#
def printMenu():
    print("--------- please choose which part to apply ---------")
    print("1: enter rule")
    print("2: run random rules")
    print("3: size estimation")
    print("4: exit")
    userinput = input("please select your number: ")
    return userinput


##**** Function read file line by line ****#
def readFile():
    global Schema_R, Schema_S

    f = open("statistics.txt", "r")
    while True:
        line = f.readline()
        if not line:
            break
        line = line.replace("\n", "")
        if line == "Scheme R":
            flag = True
        if line == "Scheme S":
            flag = False
        index = line.find("=")
        if line.startswith("V("):
            if flag:
                Schema_R.insertCol(line[2], int(line[index + 1:]))
            else:
                Schema_S.insertCol(line[2], int(line[index + 1:]))
        if line.startswith("n_R"):
            Schema_R.insertNumOfRows(int(line[index + 1:]))
        if line.startswith("n_S"):
            Schema_S.insertNumOfRows(int(line[index + 1:]))
        if line.startswith("S("):
            Schema_S.indsertRowSize(len(find_all(line, "INTEGER")) * 4)
        if line.startswith("R("):
            Schema_R.indsertRowSize(len(find_all(line, "INTEGER")) * 4)
    f.close()


##**** Function removes bruckets and whitespaces ****#
def get_value_with_no_whitespace_and_bruckets(value: str):
    return value.strip().replace(WHITESPACE, EMPTY).replace(OPEN_BRACKET, EMPTY).replace(CLOSE_BRACKET, EMPTY)


##**** Function check if condition related to the R or S tables ****#
def is_condition_of_table(condition: str, table: str):
    conditonlist = condition.replace(WHITESPACE, EMPTY).replace(AND_EXPRESSION.strip(), WHITESPACE).replace(OR_EXPRESSION.strip(), WHITESPACE).replace(
        OPEN_BRACKET, WHITESPACE).replace(CLOSE_BRACKET, WHITESPACE).strip().split()
    for i in conditonlist:
        if table == "R":
            if is_simple_condition(i, R_COL) is False:
                return False
        elif table == "S":
            if is_simple_condition(i, S_COL) is False:
                return False
        else:
            return False
    return True


##**** Function check if condition operator is good for NJOIN ****#
def is_equal_condition_natural_join(condition: str):
    list_values = condition.replace(EQUAL_SIGN, WHITESPACE).replace(COMMA_SIGN, WHITESPACE).replace(AND_EXPRESSION,
                                                                                                    WHITESPACE).replace(
        OPEN_BRACKET, WHITESPACE).replace(CLOSE_BRACKET, WHITESPACE).strip().split()
    i = 0

    flag1 = False
    flag2 = False
    proper_vals = ["R.D", "S.D", "R.E", "S.E"]
    while i < len(list_values):
        if i + 1 < len(list_values):
            if list_values[i] == "R.D":
                if list_values[i + 1] == "S.D":
                    flag1 = True
                else:
                    return False
            elif list_values[i] == "S.D":
                if list_values[i + 1] == "R.D":
                    flag1 = True
                else:
                    return False
            elif list_values[i] == "R.E":
                if list_values[i + 1] == "S.E":
                    flag2 = True
                else:
                    return False
            elif list_values[i] == "S.E":
                if list_values[i + 1] == "R.E":
                    flag2 = True
                else:
                    return False
            elif list_values[i] not in proper_vals:
                return False
        i += 2
    return flag1 and flag2


##**** Function swap two nodes ****#     A<-> prev <-> cur <-> B    to   A<-> cur <-> prev <-> B
def swapNodes(list: SLinkedList, prevNode: Node, currNode: Node):

    A = prevNode.prev
    B = currNode.next
    if list.head == prevNode:
        list.head = currNode
    else:
        A.next = currNode
    if type(B) is Node:
        B.prev = prevNode

    prevNode.prev = currNode
    prevNode.next = B
    currNode.next = prevNode
    currNode.prev = A


##**** Function check if cond ONLY from ceratin table ****#
def isCondOnlyFromTable(cond: str, tables_node: Node):
    set_values = set(cond.replace(EQUAL_SIGN, WHITESPACE).replace(COMMA_SIGN, WHITESPACE).replace(AND_EXPRESSION,
                                                                                                  WHITESPACE).replace(
        OR_EXPRESSION, WHITESPACE).replace(CLOSE_BRACKET, WHITESPACE).replace(OPEN_BRACKET, WHITESPACE).strip().split())
    value_list: list[str] = []

    for i in set_values:
        if not is_int(i):
            value_list.append(i)

    tables_col = []
    if tables_node.type is Type.PI:
        tables_col += tables_node.value.replace(EQUAL_SIGN, WHITESPACE).replace(COMMA_SIGN, WHITESPACE).replace(
            AND_EXPRESSION, WHITESPACE).replace(OR_EXPRESSION, WHITESPACE).replace(CLOSE_BRACKET, WHITESPACE).replace(
            OPEN_BRACKET, WHITESPACE).strip().split()
    else:
        if "R" in tables_node.value:
            tables_col += R_COL
        if "S" in tables_node.value:
            tables_col += S_COL

    for i in value_list:
        if i not in tables_col:
            return False
    return True


############# Main Functions #############
# **** Part One ****#
def run_part_one(queryList: SLinkedList):
    print(BOUNDARY_LINE + "Run Part One: Optimization Rules" + BOUNDARY_LINE + "\n")
    rule = input("Enter Your Rule (4, 4a, 5a, 6, 6a, 11b): ")
    rule_list = ["4", "4a", "5a", "6", "6a", "11b"]
    if rule in rule_list:
        execute_rule(rule, queryList)
        print("After Rule " + rule + ": ")
        queryList.print()
    else:
        print("Wrong input!")


# **** Part Two ****#
def run_part_two(queryList: SLinkedList):
    global list_of_queries

    print(BOUNDARY_LINE + "Run Part Two: Logical Query Plans" + BOUNDARY_LINE + "\n")
    list_of_queries = []
    for i in range(0, 4):
        list_of_queries.append(copy.deepcopy(queryList))
        print(BOUNDARY_LINE + "Run number #" + str(i+1) +BOUNDARY_LINE)
        print("Base Query: ", end="")
        queryList.print()
        for j in range(0, 10):
            rule = rand_rule()
            execute_rule(rule, list_of_queries[i])
            print("After Rule: " + rule)
            list_of_queries[i].print()


# **** Part Three ****#
def run_part_three(queryList):
    global list_of_queries, Schema_R, Schema_S, Schema_Iteration
    if len(list_of_queries) != 4:
        run_part_two(queryList)

    readFile()

    tempR = copy.deepcopy(Schema_R)
    tempS = copy.deepcopy(Schema_S)
    print(BOUNDARY_LINE + "Run Part Three: Size Estimation" + BOUNDARY_LINE + "\n")
    index = 0
    for query in list_of_queries:
        print(BOUNDARY_LINE + "Run number #" + str(index) +BOUNDARY_LINE)
        print("Size Estimation for: ", end="")
        query.print()
        run_input_output_data(query.head, None)
        Schema_R = copy.deepcopy(tempR)
        Schema_S = copy.deepcopy(tempS)
        index +=1
        Schema_Iteration = 0


# **** Parshing valid Sql Query to logic tree list ****#
def Parse_Sql_To_Logic_Tree_List(user_query: str):
    idx_select = user_query.find("SELECT")
    idx_from = user_query.find("FROM")
    idx_where = user_query.find("WHERE")
    userselect = user_query[idx_select + len("SELECT"):idx_from].replace(WHITESPACE, EMPTY)
    userselect= userselect.replace("DISTINCT", "")
    userfrom = user_query[idx_from + len("FROM"):idx_where].replace(WHITESPACE, EMPTY)
    userwhere = user_query[idx_where + len("WHERE"):len(user_query) - 1].strip()
    listNode = SLinkedList()
    if userselect.strip() == MULTIPLY_SIGN:
        userselect = ""
        added = False
        if userfrom.find("S") != -1:
            added = True
            userselect += ','.join(S_COL)
        if userfrom.find("R") != -1:
            if added:
                userselect += ","
            userselect += ','.join(R_COL)

    e1 = Node(Type.PI, userselect)
    e2 = Node(Type.SIGMA, userwhere)
    e3 = Node(Type.CARTESIAN, userfrom)
    e1.insertInside(e2)
    e2.insertInside(e3)
    listNode.head = e1
    return listNode


# *** Rule: 4 ***#
def exec_rule_four(curNode: Node):
    global INDEX_RULE_4
    INDEX_RULE_4 = 0
    flag = False
    if curNode is None:
        return False

    if curNode.type is Type.NJOIN or curNode.type is Type.CARTESIAN:
        if type(curNode.left) is Node:
            flag = exec_rule_four(curNode.left)
        if type(curNode.right) is Node and flag is False:
            flag = exec_rule_four(curNode.right)
        return flag

    if curNode.type is not Type.SIGMA:
        exec_rule_four(curNode.next)
    else:
        table_list = R_COL + S_COL
        flag_cond = is_condition(curNode.value, table_list)
        if flag_cond and INDEX_RULE_4 != 0 and curNode.value[INDEX_RULE_4:].startswith(
                AND_EXPRESSION):  # index is of and op
            left_condition = curNode.value[0:INDEX_RULE_4]
            right_condition = curNode.value[INDEX_RULE_4 + len(AND_EXPRESSION):]
            left_condition = remove_bad_brucket(left_condition)
            right_condition = remove_bad_brucket(right_condition)
            curNode.value = left_condition
            newNode = Node(Type.SIGMA, right_condition)
            curNode.insertInside(newNode)
            return True
        else:
            exec_rule_four(curNode.next)


# *** Rule: 4a ***#
def exec_rule_four_a(head: Node):
    prevNode = None
    currNode = head
    flag = False
    while currNode is not None:
        if prevNode is not None:
            if currNode.type is Type.NJOIN or currNode.type is Type.CARTESIAN:
                if type(currNode.left) is Node:
                    flag = exec_rule_four_a(currNode.left)
                if type(currNode.right) is Node and flag is False:
                    flag = exec_rule_four_a(currNode.right)
                return flag
            if prevNode.type is Type.SIGMA and currNode.type is Type.SIGMA:
                temp = prevNode.value
                prevNode.value = currNode.value
                currNode.value = temp
                return True
        prevNode = currNode
        currNode = currNode.next
    return False


# *** Rule: 5a ***#
def exec_rule_five(list: SLinkedList):
    prevNode = None
    currNode = list.head
    flag = False
    while currNode is not None:
        if prevNode is not None:
            if prevNode.type is Type.PI and currNode.type is Type.SIGMA:
                if currNode.next is not None and isCondOnlyFromTable(currNode.value, prevNode):
                   # if currNode.next.type is Type.CARTESIAN or currNode.next.type is Type.NJOIN:
                    swapNodes(list, prevNode, currNode)
                    return
        prevNode = currNode
        currNode = currNode.next

    return


# *** Rule: 6 and 6a ***#
def exec_rule_six(listNode: SLinkedList, side: str):
    prevNode = None
    flag = False
    currNode = listNode.head
    while currNode is not None:
        if prevNode is not None:
            if prevNode.type is Type.SIGMA and ((currNode.type is Type.NJOIN) or (currNode.type is Type.CARTESIAN)):
                if side == "left":

                    if is_condition_of_table(prevNode.value, currNode.left):
                        prevNode.left = currNode.left
                        currNode.left = prevNode
                        flag = True

                if side == "right":
                    if is_condition_of_table(prevNode.value, currNode.right):
                        prevNode.right = currNode.right
                        currNode.right = prevNode
                        flag = True
                if flag:
                    currNode.prev = prevNode.prev
                    prevNode.next = None
                    prevNode.prev.next = currNode
                    break
        prevNode = currNode
        currNode = currNode.next


# *** Rule: 11b ***#
def exec_rule_eleven_b(listNode: SLinkedList):
    prevNode = None
    currNode = listNode.head
    while currNode is not None:
        if prevNode is not None:
            if prevNode.type is Type.SIGMA and currNode.type is Type.CARTESIAN:
                if is_equal_condition_natural_join(prevNode.value):
                    currNode.type = Type.NJOIN
                    currNode.left = get_value_with_no_whitespace_and_bruckets(currNode.value)[0]
                    currNode.right = get_value_with_no_whitespace_and_bruckets(currNode.value)[2]
                    prevNode.prev.next = currNode
                    currNode.prev = prevNode.prev
                    break
        prevNode = currNode
        currNode = currNode.next


# *** General - Auxilary - get rule ***#
def execute_rule(rule, querylist):
    if rule == "4":
        exec_rule_four(querylist.head)
    if rule == "4a":
        exec_rule_four_a(querylist.head)
    if rule == "5a":
        exec_rule_five(querylist)
    if rule == "6":
        exec_rule_six(querylist, "left")
    if rule == "6a":
        exec_rule_six(querylist, "right")
    if rule == "11b":
        exec_rule_eleven_b(querylist)

# *** Part Three - print the report data (input/output) ***#
def run_input_output_data(currNode: Node, nodeType):
    global SchemaIO
    if currNode == None:
        return

    run_input_output_data(currNode.next, nodeType)
    print(EMPTY)
    if currNode.type == Type.CARTESIAN or currNode.type == Type.NJOIN:
        SchemaIO = calculte_print_njoin_or_cartesian(currNode)
    if currNode.type == Type.SIGMA:
        SchemaIO = calculte_print_sigma(currNode, nodeType)
    if currNode.type == Type.PI:
        SchemaIO = calculte_print_pi(currNode)