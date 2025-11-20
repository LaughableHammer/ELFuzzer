#include <stdio.h>
#include <unistd.h>

void win() {
    execve("/bin/sh", NULL, NULL);
}

void vuln() {
    char buffer[256];
    fgets(buffer, sizeof(buffer),stdin);
    printf(buffer);
}

int main() {
    printf("I love format strings!\n");
    vuln();
    return 0;
}