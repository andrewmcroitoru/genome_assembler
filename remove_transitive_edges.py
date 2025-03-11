#!/usr/bin/env python

"""
    usage:
        remove_transitive_edges [options] graph.dot
    where the options are:
        -h,--help : print usage and quit

    graph.dot is a file with a directed graph. The first row is always
        
        Digraph G {

    and the last row is always 

        }

    Each row in the middle section describes an edge. For example,

        1 -> 2

    is a directed edge from a node with the label '1' to the node with the label    '2'.
"""

from sys import argv, stderr
from getopt import getopt, GetoptError
from copy import deepcopy
from graph import *

def get_children(G: Graph, parent: str) -> list:
    # Assumes G has node parent
    return list(G.edges[parent].keys())


def simplify(G: Graph, debug: bool = False) -> Graph:
    """Simplify the graph S by removing the transitively-inferrible edges.

    S is just a copy of G, which is the input to the graph. 
    """
    # Copy of the input graph that this function mutates by removing TI edges. 
    S: Graph = deepcopy(G)
    nodes: list = S.nodes()

    # BRUTE FORCE APPROACH: For each node i, perform a BFS and remove all edges i->j where j is visited during the bfs i more than once  
    for starting_node in nodes:
        print(f"\n\n=== Starting Node: {starting_node} ===") if debug else None
        # Initialize variables for this starting node
        parent_nodes: list = []
        curr_depth: int = 0
        visited_nodes: set = set()

        # If on the first iteration, set the starting node as parent_nodes
        if curr_depth == 0:
            parent_nodes = [starting_node]

        continue_loop: bool = True
        while continue_loop:
            print(f"\n{curr_depth}\tvisited_nodes: {visited_nodes}") if debug else None
            ## For the current nodes, follow the steps i-iii:
            # i) Check which nodes have already been visited
            new_nodes_visited_this_iter: list = [node for node in parent_nodes if node not in visited_nodes]
            already_visited_nodes: list = list(set(parent_nodes).intersection(visited_nodes)) # in parent nodes and visited nodes
            print(f"{curr_depth}\tnew_nodes_visited_this_iter: {new_nodes_visited_this_iter}") if debug else None
            print(f"{curr_depth}\talready_visited_nodes: {already_visited_nodes}") if debug else None
            # ii) Mark newly visited parent nodes as visited. Get list of unvisited nodes's children on which to recurse. 
            visited_nodes = visited_nodes.union(set(new_nodes_visited_this_iter))
            print(f"{curr_depth}\tvisited_nodes': {visited_nodes}") if debug else None
            # Get all children on which to recurse 
            curr_depth_children: set = set() # keep track of all children visited this iteration
            for node in new_nodes_visited_this_iter: 
                # for each node at curr_depth, get its children
                curr_children: list = get_children(G, node)
                for child in curr_children:
                    # for each child, if it has been visited, do not visit it next iteration.
                    if child not in curr_depth_children:
                        curr_depth_children.add(child)
            print(f"{curr_depth}\tcurr_depth_children: {curr_depth_children}") if debug else None
            # iii) For all nodes in parent_nodes that were already visited, remove any edge in G from starting_node to an already visited node 
            for node in already_visited_nodes:
                print(f"Removing any {starting_node} -> {node} edges") if debug else None
                S.delete_edge(starting_node, node)
                
            # Check to see if there will be another iteration
            if len(curr_depth_children) == 0 : # ran out of nodes to visit
                print(f"{curr_depth}\tRan out of nodes to visit!") if debug else None
                continue_loop = False
            elif (curr_depth > 0) and (starting_node in parent_nodes): # we are in a cycle!
                print(f"{curr_depth}Cycle!") if debug else None
                continue_loop = False
            else:
                 # Update for next iteration
                parent_nodes=list(curr_depth_children)
                curr_depth=curr_depth + 1
                visited_nodes=visited_nodes
        
        print(f"!!! Stopping at depth = {curr_depth - 1} !!!") if debug else None

    return S   


def main(filename):
    # read the graph from the input file
    graph = Graph(filename)
    print(f"Read the graph from {filename}", file=stderr)

    # simplify the graph by removing the transitively-inferrible edges
    simplified = simplify(graph)
    print(f"Simplified the graph", file=stderr)

    # print the simplified graph in the same format as the input file
    print(simplified)

if __name__ == "__main__":
    edges = {
        "A":{"B":1, "C":1, "D":1},
        "B":{"C":1},
        "C":{"D":1}
    }
    G = Graph(edges)
    bfs_to_depth(G, ['A'], depth = 4)
    # try:
    #     opts, args = getopt(argv[1:], "h", ["help"])
    # except GetoptError as err:
    #     print(err)
    #     print(__doc__, file=stderr)
    #     exit(1) 

    # for o, a in opts:
    #     if o in ("-h", "--help"):
    #         print(__doc__, file=stderr)
    #         exit()
    #     else:
    #         assert False, "unhandled option"

    # if len(args) != 1:
    #     print(__doc__, file=stderr)
    #     exit(2)

    # main(args[0])
