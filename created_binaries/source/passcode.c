#include <stdio.h>
#include <string.h>

int main(void) {
    printf("Hello, please enter code to enter secret blog\n");

    int code;
    scanf("%d", &code);

    char post[100];

    if (code == 1234) {
        printf("You have unlocked the blog! What would you like to write?");
        fgets(post, 0x100, stdin);

        printf("How very insightful");
    }

    return 0;
}
