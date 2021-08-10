#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main() {
	ifstream infile("test1.tsv");
	string line;
	
	while (getline(infile, line)) {
		cout << line << "\n";
	}
}
