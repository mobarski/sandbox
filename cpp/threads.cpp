#include <thread>
#include <iostream>
using namespace std;

int X[] = {55,66,77,88,99};

void foo(int x) {
	cout << "hello" << x << X[1] <<"\n";
}

int main() {
	thread t1(foo,42);
	thread t2(foo,22);
	thread t3(foo,12);
	t3.join();
	t2.join();
	t1.join();
}
