#include <stdio.h>

void vuln() {
    char buffer[256];
    fgets(buffer, 500,stdin);
}

int main() {   
    vuln();

    // ensure we are only detecting crashes
    fprintf(stderr, "not a real crash");
    return -6;
}