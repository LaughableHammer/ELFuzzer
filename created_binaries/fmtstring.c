#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int secret = 0x41414141;

int main(void) {
    char buffer[128];

    printf("Enter something:\n");
    fflush(stdout);

    fgets(buffer, sizeof(buffer), stdin);
    printf(buffer);

    if (strstr(buffer, "CRASH") != NULL) {
        char *p = NULL;
        *p = 'X';
    }

    return 0;
}
