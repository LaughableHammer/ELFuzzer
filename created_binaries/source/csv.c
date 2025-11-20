#include <stdio.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char* getfield(char* line, int num)
{
    const char* tok;
    for (tok = strtok(line, ",");
            tok && *tok;
            tok = strtok(NULL, ",\n"))
    {
        if (!--num)
            return tok;
    }
    return NULL;
}

int main()
{
    char line[1000];
    char buff[10];
    while (fgets(line, 1000, stdin))
    {
        char* tmp = strdup(line);
        const char* val = getfield(tmp, 3);
        strcat(buff, val);
        free(tmp);
    }

    return 0;
}