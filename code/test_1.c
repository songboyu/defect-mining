#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

void test (char *buf) {
    if(strcmp(buf, "songboyu") == 0) {
        raise(SIGSEGV);
    }
}

int main()
{
    char buf[5];
    scanf("%8c", &buf);

    test(buf);
    return 0;
}