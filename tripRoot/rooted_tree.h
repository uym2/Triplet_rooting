#ifndef ROOTED_TREE_H
#define ROOTED_TREE_H

#include <iostream>
#include <vector>
#include <map>
#include <string>
#include "int_stuff.h"
#include "templated_linked_list.h"
#include "TripletCounter.h"

class HDT;// Forward declaration...
class RootedTreeFactory; // Forward declaration...

using namespace std;

class RootedTree
{
	public:
        unsigned int idx; // added by uym2
		unsigned int level;
		RootedTree *parent;
		TemplatedLinkedList<RootedTree*> *children;
		string name;
		unsigned int numChildren;
		int maxDegree;
		RootedTree *altWorldSelf;
		HDT *hdtLink;
		int color;
		INTTYPE_REST numZeroes;

		RootedTreeFactory *factory;

		// How many leaves beneath you?
		int n;

        int set_idx (unsigned int idx) { this->idx = idx; return 0; }; // uym2 added
        int set_all_idx (unsigned int startIdx); // uym2 added
        RootedTree* down_root(RootedTree *u); // uym2 added
        void print_leaves(); // uym2 added
        RootedTree* copyTree(RootedTreeFactory *factory = NULL);
        RootedTree* reroot_at_edge(RootedTree *node);
        void write_newick(ofstream &fout);
        bool remove_child(RootedTree *child);
        
		void initialize(string name);
		bool isLeaf();
		void addChild(RootedTree *t);
		RootedTree* getParent();
		INTTYPE_REST getUnresolvedTriplets();
		INTTYPE_N4 getUnresolvedQuartets();
		void toDot();
		vector<RootedTree*>* getList();
		void pairAltWorld(RootedTree *t, bool do_pruning=true, TripletCounter *tripCount=NULL);
		void colorSubtree(int c);
		void markHDTAlternative();
		bool isError();
		RootedTree *contract(RootedTreeFactory *factory = NULL);
        bool prune_subtree(RootedTree* leaf);
        void mark_active(TripletCounter *tripCount);
           
    private:
		bool error;

		void toDotImpl();
		void getListImpl(vector<RootedTree*>* list);
		void computeNullChildrenData();
		RootedTree* contractImpl(RootedTreeFactory *factory);
        void __write_newick__(ofstream &fout);
};

#endif
