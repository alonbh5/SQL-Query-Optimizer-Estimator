from funcs import *

def main():
    user_input = input("Enter Your SQL Query: ").strip()
    logic_tree_list = Parse_Sql_To_Logic_Tree_List(user_input)
    print("\nLogic Tree")
    print(BOUNDARY_LINE)
    logic_tree_list.print()
    logic_tree_list_copy = copy.deepcopy(logic_tree_list)
    while(1):
        userSelection = printMenu()
        if userSelection == "1":
            run_part_one(logic_tree_list_copy)
        elif userSelection == "2":
            run_part_two(logic_tree_list)
        elif userSelection == "3":
            run_part_three(logic_tree_list)
        elif userSelection == "4":
            break
        else:
            print("Wrong Input, Please try again!")

    print("BYE!")
    return


main()