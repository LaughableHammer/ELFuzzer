#include <stdio.h>

void vuln() {
    char buffer[256];
    fgets(buffer, 500,stdin);
}

int main() {   
    vuln();
    fprintf(stderr, "stack smashing detected");
    return -6;
}