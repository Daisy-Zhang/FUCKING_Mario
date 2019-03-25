#include "SimSearcher.h"

using namespace std;

int main(int argc, char **argv)
{
	SimSearcher searcher;

	vector<pair<unsigned, unsigned> > resultED;
	vector<pair<unsigned, double> > resultJaccard;

	unsigned q = 2, edThreshold = 6;
	double jaccardThreshold = 0.4;

	if(searcher.createIndex(argv[1], q) == SUCCESS) {
		printf("create index \n");
	}
	if(searcher.searchJaccard("query query e", jaccardThreshold, resultJaccard) == SUCCESS){
		printf("search Jaccard \n");
	}
	/*if(searcher.searchED("query", edThreshold, resultED) == SUCCESS) {
		printf("search ED\n");
	}*/
	return 0;
}

