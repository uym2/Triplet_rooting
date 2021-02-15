from tqdist import *
from triproot import *
from tripVote.tripvote_lib import reroot_at_edge,tripVote 
from treeswift import *
from math import log2, ceil

def prune_long(tree,max_depth):
    cutting_list = []
    for node in tree.traverse_preorder():
        if node.is_root():
            node.depth = 0
        else:
            node.depth = node.get_parent().depth + 1
        if node.depth == max_depth+1:
            cutting_list.append(node)
    while cutting_list:
        node = cutting_list.pop()
        p = node.get_parent()
        if p is not None:
            p.remove_child(node)
            if p.is_leaf():
                cutting_list.append(p)
    tree.suppress_unifurcations()
                

def place_one_taxon(myTree,refTrees,missing_taxon,max_depth='max'):
# remove all trees in refTrees that do not have the missing_taxon
# and assume myTree is missing the missing_taxon
# myTree: a newick string. Assume it has unique labeling for all nodes
# refTrees: a list of newick strings
# missing_taxon: a leaf label (string)
# max_depth: only count the triplets with depth up to max_depth.
# Special case:     max_depth = 'max': include all triplets (default)
#                   max_depth = 'log2': ceil(log2(n)) where n is the number of leaves

    rerooted_refTrees = []
    #W = []
    i = 0
    for rstr in refTrees:
        tree_obj = read_tree_newick(rstr)
        n = len(list(tree_obj.traverse_leaves()))
        if max_depth == 'max':
            d = n
        elif max_depth == 'log2':
            d = ceil(log2(n))
        else:
            d = int(max_depth)    
        new_root = None
        for leaf in tree_obj.traverse_leaves():
            if leaf.label == missing_taxon:
                new_root = leaf
                break     
        if new_root is not None:
            reroot_at_edge(tree_obj,new_root,new_root.edge_length/2)  
            C = tree_obj.root.children
            c_star = None
            for c in C:
                if c.label == missing_taxon:
                    c_star = c
                    break
            if c_star is not None:
                tree_obj.root.remove_child(c_star) 
            tree_obj.suppress_unifurcations()
            if d < n:
                prune_long(tree_obj,d)    
            if (len(list(tree_obj.traverse_leaves())) >= 3):
                rerooted = tree_obj.newick()
                rerooted_refTrees.append(rerooted)

    _,_,placement_label = tripVote(myTree,rerooted_refTrees)
    tree_obj = read_tree_newick(myTree)
    placement_node = None
    for node in tree_obj.traverse_preorder():
        if node.label == placement_label:
            placement_node = node
            break
    node = placement_node
    d = 0
    while not node.is_root():
        node = node.get_parent()
        d += 1
    return placement_label, d                    
