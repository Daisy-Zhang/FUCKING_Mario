#include "SimSearcher.h"
#include <cstdlib>

using namespace std;

inline bool greater_second(const pair<int, int> &p1, const pair<int, int> &p2) {
	return p1.second > p2.second;
}

inline int inline_min(int a, int b) {
	if(a >= b) {
		return b;
	}
	else {
		return a;
	}
}

inline int calED_T(int len, int q, int thre) {
	return  len + 1 - q - thre * q;
}

inline int calJac_T(int query_size, double threhold, int smin) {
	double res1 = threhold * query_size;
	double res2 = (query_size + smin) * threhold / (1 + threhold);
	return ceil(res1) > ceil(res2) ? ceil(res1) : ceil(res2);
}

double getJaccard(vector<string> &a, vector<string> &b) {
	int both = 0;

	for(auto word : a) {
		if(find(b.begin(), b.end(), word) != b.end()) {
			both ++;
		}
	}

	return (double)both / (double)(a.size() + b.size() - both);
}

SimSearcher::SimSearcher()
{
}

SimSearcher::~SimSearcher()
{
}

int SimSearcher::createIndex(const char *filename, unsigned q)
{
	record.clear();
	str_id.clear();

	qgram = q;
	FILE *fp = fopen(filename, "r");
	char s[1024];
	while((fgets(s, 1024, fp)) != NULL) {
		s[strlen(s) - 1] = '\0';
		//string str = s;
		record.push_back(s);
	}
	record_ans = record.size();
	//record_count = new int[record_ans];
	//flag_count = new int[record_ans];
	flag = 0;
	memset(&flag_count, 0, sizeof(int) * record_ans);
	//memset(record_count, 0, sizeof(int) * record_ans);

	// ED: 建立倒排
	for(int i = 0; i < record_ans; i ++) {
		string record_str = record[i];
		for(int j = 0; j <= record_str.length() - qgram; j ++) {
			ED_Trie.insert(record_str.substr(j, qgram).c_str(), qgram, i);
		}
	}

	// Jaccard: 建立倒排，包含去重
	for(int i = 0; i < record_ans; i ++) {
		string record_str = record[i];
		int last_pos = 0;
		int ans = 0;
		//cout << record_str << endl;
		for(int j = 0; j < record_str.length(); j ++) {
			if(record_str[j] == ' ') {
				string tmp = record_str.substr(last_pos, j - last_pos);
				if(str_id[tmp] != i + 1) {
					str_id[tmp] = i + 1;
					Jac_Trie.insert(tmp.c_str(), j - last_pos, i);
					ans ++;

					line_word[i].push_back(tmp);
					//cout << "*" << tmp << endl;
				}
				last_pos = j + 1;
			}
			else if(j == record_str.length() - 1) {
				string tmp = record_str.substr(last_pos, j + 1 - last_pos);
				if(str_id[tmp] != i + 1) {
					Jac_Trie.insert(tmp.c_str(), j - last_pos + 1, i);
					ans ++;

					line_word[i].push_back(tmp);
					//cout << "*" << tmp << endl;
				}
			}
		}
		if(ans < Smin) {
			Smin = ans;
		}
	}

	return SUCCESS;
}

int SimSearcher::searchJaccard(const char *query, double threshold, vector<pair<unsigned, double> > &result)
{
	result.clear();
	flag ++;

	/*for(int i = 0; i < record_ans; i++) {
		cout << i << " " << endl;
		for(int j = 0 ; j < line_word[i].size(); j ++) {
			cout << line_word[i][j] << endl;
		}
		cout << endl;
	}*/

	// 输入的query分词操作，包含去重
	string str_query = query;
	vector<string> query_set;
	int last_pos = 0;
	for(int i = 0; i < str_query.length(); i ++) {
		if(str_query[i] == ' ') {
			string tmp = str_query.substr(last_pos, i - last_pos);
			if(str_id[tmp] != QUERY_MAP_NUM) {
				query_set.push_back(tmp);
				//cout << "!" << tmp << endl;
				str_id[tmp] = QUERY_MAP_NUM;
			}
			last_pos = i + 1;
		}
		else if(i == str_query.length() - 1) {
			string tmp = str_query.substr(last_pos, i + 1 - last_pos);
			if(str_id[tmp] != QUERY_MAP_NUM) {
				//cout << "!" << tmp << endl;
				query_set.push_back(tmp);
			}
		}
	}
	
	vector<vector<int> *> query_jac_index_list;			// 存下query分词后每一个分词对应的record倒排列表
	vector<pair<int, int>> query_jac_index_size;		// 存下找到的每个分词在上一行vec中的索引和vec大小

	int index_ans = 0;
	for(auto word : query_set) {
		vector<int> *search_res =  Jac_Trie.search(word.c_str(), word.length());

		if(search_res) {
			//cout << "! " << query_set[i] << endl;
			query_jac_index_list.push_back(search_res);
			query_jac_index_size.push_back(make_pair(index_ans, search_res -> size()));
			index_ans ++;
		}
	}

	int T = calJac_T(query_set.size(), threshold, Smin);
	//cout << "!" << T << endl;

	vector<int> tar_record;
	
	if(T <= 0) {
		for(int i = 0; i < record_ans; i ++) {
			tar_record.push_back(i);
		}
	}
	else {
		sort(query_jac_index_size.begin(), query_jac_index_size.end(), greater_second);

		/*for(int i = 0; i  < query_jac_index_size.size(); i ++) {
			cout << query_jac_index_size[i].first << " " << query_jac_index_size[i].second << endl;
		}*/

		vector<int> short_all;				// 短链里面出现的string-id
		register int index = 0;
		for(int i = T - 1; i < query_jac_index_size.size(); i ++) {
			// short list
			index = query_jac_index_size[i].first;
			//cout << "!" << index << endl;
			for(auto id : *(query_jac_index_list[index])) {
				//cout << id << " ";
				if(flag_count[id] != flag) {
					record_count[id] = 0;
					flag_count[id] = flag;
					short_all.push_back(id);
				}
				record_count[id] ++;
			}
		}

		// binary search in long list
		register int times(0);
		register int id_T(0);
		register int k(0);
		for(auto id : short_all) {
			times = record_count[id];

			for(int j = 0; j < T - 1; j ++) {
				if(T - 2 - j + 1 < T - times) {
					break;
				}
				
				int k = query_jac_index_size[j].first;

				if (binary_search(query_jac_index_list[k] -> begin(), query_jac_index_list[k] -> end(), id)){
					times ++;
				}
			}

			if(times >= T) {
				tar_record.push_back(id);
			}
		}
		sort(tar_record.begin(), tar_record.end());
	}

	// 暴力扫一趟算出交集，精确计算
	for(auto id : tar_record) {
		double jaccard = getJaccard(query_set, line_word[id]);
		if(jaccard >= threshold) {
			//cout << id << " " << jaccard << endl;
			result.push_back(make_pair(id, jaccard));
		}
	}

	return SUCCESS;
}

int SimSearcher::searchED(const char *query, unsigned threshold, vector<pair<unsigned, unsigned> > &result)
{
	result.clear();

	flag ++;
	string str_query(query);
	vector<int> tar_record;		// 存下最后的string-id

	int T = calED_T(str_query.length(), qgram, threshold);

	if(T <= 0) {
		for(int i = 0; i < record_ans; i ++) {
			tar_record.push_back(i);
		}
	}
	else {
		string str_query(query);
		vector<vector<int> *> query_qgram_index_list;
		vector<pair<int, int>> query_qgram_index_size;

		vector<int> short_all;

		register int has_res = 0;
		for(int i = 0; i <= str_query.length() - qgram; i ++) {
			vector<int> *search_res =  ED_Trie.search(query + i, qgram);
			if(search_res) {
				query_qgram_index_list.push_back(search_res);
				query_qgram_index_size.push_back(make_pair(has_res, search_res -> size()));
				
				has_res ++;
			}
		}

		sort(query_qgram_index_size.begin(), query_qgram_index_size.end(), greater_second);

		register int index = 0;
		for(int i = T - 1; i < query_qgram_index_size.size(); i ++) {
			// short list
			index = query_qgram_index_size[i].first;
			//cout << "!" << index << endl;
			for(auto id : *(query_qgram_index_list[index])) {
				//cout << id << " ";
				if(flag_count[id] != flag) {
					record_count[id] = 0;
					flag_count[id] = flag;
					short_all.push_back(id);
				}
				record_count[id] ++;
			}
		}
		// binary search in long list
		register int times(0);
		register int id_T(0);
		register int k(0);
		for(auto id : short_all) {
			times = record_count[id];

			int id_T = calED_T(record[id].length(), qgram, threshold);
			if(times + T < id_T) {
				continue;
			}

			for(int j = 0; j < T - 1; j ++) {
				if(T - 2 - j + 1 < T - times) {
					break;
				}
				
				int k = query_qgram_index_size[j].first;

				if (binary_search(query_qgram_index_list[k] -> begin(), query_qgram_index_list[k] -> end(), id)){
					times ++;
				}
			}

			if(times >= T) {
				tar_record.push_back(id);
			}
		}

		sort(tar_record.begin(), tar_record.end());
	}

	for(int i = 0; i < tar_record.size(); i ++) {
		int id = tar_record[i];
		int row = str_query.length() + 1;
		int col = record[id].length() + 1;
		int matrix[row][col];
		for(int m = 0; m <= row - 1; m ++) {
			for(int n = 0; n <= col - 1; n ++) {
				if(m == 0) {
					matrix[m][n] = n;
				}
				else if(n == 0) {
					matrix[m][n] = m;
				}
				else {
					matrix[m][n] = inline_min(matrix[m - 1][n] + 1, matrix[m][n - 1] + 1);
					int t = 0;
					if(str_query[m - 1] != record[id][n - 1]) {
						t = 1;
					}
					matrix[m][n] = inline_min(matrix[m][n], matrix[m - 1][n - 1] + t);
				}
			}
		}
		int final_res  = matrix[row - 1][col - 1];
		if(final_res <= threshold) {
			result.push_back(make_pair(id, final_res));
		}
	}

	return SUCCESS;
}