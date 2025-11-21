#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int small = 10;
    char *chunk1 = malloc(small);
    char *chunk2 = malloc(small); 

    printf("overflow the chunk: ");
    fgets(chunk1, 100, stdin);

    free(chunk2);
    free(chunk1);
    return 0;
}