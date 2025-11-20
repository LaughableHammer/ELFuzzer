#include <stdio.h>

void vuln() {
    char buffer[256];
    fgets(buffer, 500,stdin);
}

int main() {   
    vuln();
    return 0;
}