#include <string>
#include <iostream>
#include <unordered_map>

using namespace std;

int main() {
	unordered_map<string,int> m { {"a",11}, {"b",22}, {"c",33} };
	cout << m["a"] << "\n";
	m["x"] = 123;
	cout << m["x"] << "\n";
	cout << m["y"] << "\n";
}

