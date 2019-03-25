#pragma once
#include <vector>
#include <utility>
#include <fstream>
#include <string>
#include <cstdio>
#include <vector>
#include <algorithm>
#include <iostream>
#include <cstring>
#include <unordered_map>

using namespace std;

const int SUCCESS = 0;
const int FAILURE = 1;

const int CHILD_MAX = 128;
const int QUERY_MAP_NUM = 10000000;

struct TrieNode
{
    bool is;					// 是否为一个gram
    TrieNode *child[CHILD_MAX];		// ASCII字符
    vector<int> index_list;				// 倒排表

    TrieNode() : is(false)
    {
        for (int i = 0; i < CHILD_MAX; i++)
            child[i] = NULL;
        index_list.clear();
    }
};

struct Trie
{
    TrieNode *root;

    Trie() {
        root = new TrieNode();
    }

	// str: gram, len: length(str), index: str-id
    void insert(const char* str, int len, int index) {
        TrieNode *node = root;
        for (int i = 0; i < len; i++) {
            if (!node -> child[(int)str[i]]) {
                node -> child[(int)str[i]] = new TrieNode();
            }
            node = node -> child[(int)str[i]];
        }
        node -> is = true;
        if (node -> index_list.empty() || *(node -> index_list.end() - 1) != index)		// 包含去重
            node -> index_list.push_back(index);
    }

    vector<int>* search(const char* str, int len) {
        TrieNode *node = root;
        for (int i = 0; i < len; i++) {
            if(!node -> child[(int)str[i]])
                return NULL;
            node = node -> child[(int)str[i]];
        }
        if (!node)
            return NULL;
        if (!node -> is)
            return NULL;
        return &(node -> index_list);
    }
};

class SimSearcher
{
private:
	vector<string> record;
	int record_ans = 0;
	int qgram = 0;
    //int *record_count;      // 记录每一次查询中每一个string出现的次数
    //int *flag_count;        // 某条record的第几次查询
    int record_count[800000];
    int flag_count[800000];
    int flag;               // 查询次数

	Trie ED_Trie;
    Trie Jac_Trie;

    int Smin = 10000000;
	
	unordered_map<string, int> str_id;      // 用于存下分词后的每个串在哪个record中出现，用于去重，其中id存下的为i + 1
    unordered_map<int, vector<string>> line_word;

public:
	SimSearcher();
	~SimSearcher();

	int createIndex(const char *filename, unsigned q);
	int searchJaccard(const char *query, double threshold, std::vector<std::pair<unsigned, double> > &result);
	int searchED(const char *query, unsigned threshold, std::vector<std::pair<unsigned, unsigned> > &result);

};

