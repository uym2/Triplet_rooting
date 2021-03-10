#! /usr/bin/env python

import sys
import os
import argparse
import time
from tripVote.placement_lib import place_one_taxon, place_one_taxon_iter, complete_gene_trees
from statistics import median
from math import exp, log
import random
from treeswift import *

def main():
    MY_VERSION='1.0.4b'

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=True, help="Input trees")
    parser.add_argument('-o', '--output', required=True, help="Output trees")
    parser.add_argument('-v', '--version',action='version', version=MY_VERSION, help="Show program version and exit")
    
    args = parser.parse_args()

    random.seed(a=1105)

    start = time.time()
    print("Running tripVote_placement version " + MY_VERSION)
    print("tripVote_placement was called as follow: " + " ".join(sys.argv))

    with open(args.input,'r') as f:
        inputTrees = f.read().strip().split("\n")

    inputTrees_nobrlen = []
    for treeStr in inputTrees:
        tree_obj = read_tree_newick(treeStr)
        for node in tree_obj.traverse_preorder():
            node.edge_length = None
        inputTrees_nobrlen.append(tree_obj.newick())

    outputTrees = complete_gene_trees(inputTrees_nobrlen)
    with open(args.output,'w') as f:
        f.write('\n'.join(outputTrees))
    
    end = time.time()
    print("Runtime: ", end - start) 

if __name__ == "__main__":
    main()    