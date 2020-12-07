import networkx as nx
from parse import read_input_file, write_output_file, read_output_file
from utils import is_valid_solution, calculate_happiness, calculate_stress_for_room
import sys
from os.path import basename, normpath
import glob
import os
import time
import random


# def solve(G, s):
#     """
#     Args:
#         G: networkx.Graph
#         s: stress_budget
#     Returns:
#         D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
#         k: Number of breakout rooms
#     """

#     # TODO: your code here!
#     ratios = []
#     for u, v, happiness in G.edges.data("happiness"):
#         if (G[u][v]["stress"] == 0):
#             happy_to_stress_ratio = happiness
#         else:
#             happy_to_stress_ratio = happiness / G[u][v]["stress"]
#         triple = (u, v, happy_to_stress_ratio)
#         ratios.append(triple)
#     ratios = sorted(ratios, key=lambda x: x[-1])
#     D= {}
#     total_stress = 0
#     for u, v, stress in G.edges.data("stress"):
#         total_stress = total_stress + stress
#     for i in G.nodes:
#         D[i] = 0
#     rooms = 1
#     while not is_valid_solution(D, G, s, rooms):
#         for i in range(rooms):
#             people_in_room_i = [person for person in D.keys() if D[person] == i]
#             while calculate_stress_for_room(people_in_room_i, G) > s/rooms:
#                 min_ratio = float("inf")
#                 for person in people_in_room_i:
#                     my_ratio = sum([ratio[2] for ratio in ratios if ratios[0] == person])
#                     if my_ratio < min_ratio:
#                         person_to_take_out = person
#                 D[person_to_take_out] = i + 1
#                 people_in_room_i.remove(person_to_take_out)
#         rooms = rooms + 1
#     return D, rooms
#     # pass

def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    D= {}
    for i in G.nodes:
        D[i] = 0
    rooms = 1
    while not is_valid_solution(D, G, s, rooms):
        # print(rooms)
        for i in range(rooms):
            people_in_room_i = [person for person in D.keys() if D[person] == i]
            while calculate_stress_for_room(people_in_room_i, G) > s/rooms:
                person_to_take_out = people_in_room_i[random.randrange(0, len(people_in_room_i)-1, 1)]
                D[person_to_take_out] = i + 1
                if (i+1) > rooms - 1:
                    rooms = rooms + 1
                people_in_room_i.remove(person_to_take_out)     
    return D, rooms

# sorted(g.edges(data=True),key= lambda x: x[2]['callDuration'],reverse=True)

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     t_end = time.time() + 5
#     output_path = 'samples/50.out'
#     G, s = read_input_file(input_path)
    
#     # Check output file
#     savedrooms = read_output_file(output_path, G, s)
#     savedhappiness = calculate_happiness(savedrooms, G)
#     t_end = time.time() + 6
#     # Solving
#     while time.time() < t_end:
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)

#         # check if should update
#         happiness = calculate_happiness(D, G)
#         if happiness > savedhappiness:
#             write_output_file(D, output_path)
#             savedhappiness = happiness
#         else:
#             continue
    
# if __name__ == '__main__':
# assert len(sys.argv) == 1
# directory_in_str = sys.argv[1]
# directory = os.fsencode(directory_in_str)
# for file in os.listdir(directory):
#     # calculate
#     path = os.fsdecode(file)
#     number = path.split(".")[0]
#     G, s = read_input_file(path)
#     D, k = solve(G, s)
#     assert is_valid_solution(D, G, s, k)
#     cost_t = calculate_happiness(D, G)
    
#     #write file
#     output_path = "outputs/" + number + ".out"
#     write_output_file(D, output_path)
#     D = read_output_file(output_path, G, s)
#     print("Total Happiness: {}".format(cost_t))


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('test_inputs/*')
    for input_path in inputs:
        output_path = 'test_outputs/' + basename(normpath(input_path))[:-3] + '.out'
        G, s = read_input_file(input_path)
        
        # Check output file
        savedrooms = read_output_file(output_path, G, s)
        savedhappiness = calculate_happiness(savedrooms, G)

        # Find the size of file
        t_end = 0
        size = basename(normpath(input_path)).split("-")[0]
        # print(size)
        if size == "small":
            t_end = 10
        elif size == "medium":
            t_end = 50
        elif size == "large":
            t_end = 120

        t_end = time.time() + t_end
        # Solving
        while time.time() < t_end:
            D, k = solve(G, s)
            assert is_valid_solution(D, G, s, k)

            # check if should update
            happiness = calculate_happiness(D, G)
            if happiness > savedhappiness:
                write_output_file(D, output_path)
                savedhappiness = happiness
            else:
                continue
        print(savedhappiness)

#pass in 2d array of outputs where each line represents a room,
# returns a list of tuples where each tuple represents a line in the input