#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

int main()
{
    int x;
    scanf("%d", &x);
    if(x == 561237896){
    	raise(SIGSEGV);
    }
    return 0;
}
