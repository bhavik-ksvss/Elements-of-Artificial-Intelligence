#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: Bhavik Kollipara, Chandra Sagar Bhogadi, Vaishnavi RM
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import time


# The function below is used to parse through the input text file and create a list of students and a dictonary of requirements.
def parsing_file(input_file):

    stu_list = []
    stu_dict = {}
    with open(input_file, "r") as f:
        for line in f.read().rstrip("\n").split("\n"):
            print('bhavik')
            stu_dict_element = {}
            element_in_line = line.split(" ")
            print('element:',element_in_line)
            stu_list.append(element_in_line[0])
            stu_dict_element['team_size'] = len(element_in_line[1].split('-'))
            stu_dict_element['interested_teammate'] = [i for i in element_in_line[1].split('-') if i not in [element_in_line[0]] + ['zzz']]
            print('intersted_teammate',stu_dict_element['interested_teammate'])                                              
            stu_dict_element['not_interested_teammate'] = [] if element_in_line[2] == '_' else [i for i in element_in_line[2].split(',')]
            print('not_intersted_teammate',stu_dict_element['not_interested_teammate'])   
            stu_dict[element_in_line[0]] = stu_dict_element
            print('bhavik')
    return stu_list, stu_dict


# the below function is used to calculate total complain cost to form the requested team size and team members
def compute_cost(users,current_team,element):
    complain_count = 0
    for username in users:
        team = [i for i in current_team if username in i]
        complain_count=complain_count(team)*5
        if len(team) != element[username]['team_size']:
            complain_count=complain_count*2
        len_of_requested_user_not_assigned = len(set(element[username]['interested_teammate']) - set(team))
        complain_count += len_of_requested_user_not_assigned
        len_of_not_interested_user_assigned = len(
            set(element[username]['not_interested_teammate']).intersection(set(team)))
        complain_count += len_of_not_interested_user_assigned * 2
    return complain_count


def team_selection(element):
    for i in element['interested_teammate']:
        pass


    
    








def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    students, element = parsing_file(input_file)
    team_formation = []
    default_team= []
    default_team.extend([[student] for student in students])


    # Simple example. First we yield a quick solution
    yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12", "vrmath"],
               "total-cost" : 12})

    # Then we think a while and return another solution:
    time.sleep(10)
    yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12-vrmath"],
               "total-cost" : 10})

    # This solution will never befound, but that's ok; program will be killed eventually by the
    #  test script.
    while True:
        pass
    
    yield({"assigned-groups": ["vibvats-djcran", "zkachwal-shah12-vrmath"],
               "total-cost" : 9})

if __name__ == "__main__":

    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))
    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])


