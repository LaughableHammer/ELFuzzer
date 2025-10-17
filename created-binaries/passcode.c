#include <stdio.h>
#include <string.h>

int main(void) {
    printf("Hello, please enter code\n");

    int code;
    scanf("%d", &code);

    if (code == 1234) {
        printf("Here's a free crash");
        strcpy(&code, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa");
    }

    return 0;
}
