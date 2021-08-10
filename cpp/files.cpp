#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

using namespace std;

int main() {
	ifstream infile("test1.tsv");
	string line;
	
	while (getline(infile, line)) {
		stringstream ss(line);
		string word;
		while (getline(ss,word,'\t')) {
			cout << word << " - ";
		}
		cout << "\n";
	}
}
