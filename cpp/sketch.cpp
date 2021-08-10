#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
#include <unordered_map>

using namespace std;

int main() {
	unordered_map<string,vector<int>> db;
	
	ifstream infile("test2.tsv");
	string line;
	
	getline(infile, line); // skip header
	
	while (getline(infile, line)) {
		stringstream line_ss(line);
		string key;
		string val;
		getline(line_ss,key,'\t');
		getline(line_ss,val,'\t');
		
		// split val
		stringstream val_ss(val);
		string v;
		vector<int> vec;
		int num;
		while (getline(val_ss,v,',')) {
			num = stoi(v);
			vec.push_back(num);
		}
		// sort and load
		sort(vec.begin(), vec.end());
		db[key] = vec;
	}
	cout << db["ff"][0] << " ";
	cout << db["ff"][1] << " ";
	cout << db["ff"][2] << " ";
}
