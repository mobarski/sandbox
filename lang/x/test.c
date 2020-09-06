#include <stdio.h>

struct Point {
	int x;
	int y;
};

int main() {
	int z[3][4];
	z[1][2] = -1;
	void* f = fopen("usunmnie.txt","w");
	struct Point p = {.y=1,.x=2};
	fputs("Hello World!",f);
	printf("Hello! %d %d",p.x,p.y);
	return 0;
};

