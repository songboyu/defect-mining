#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

int main()
{
    int x,y;
    scanf("%d+%d", &x, &y);
    if(x == 1203789){
	if(y == 6666){
    	    raise(SIGSEGV);
	}
    }
    return 0;
}
