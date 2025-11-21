#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdint.h>

#define COM 0xfe
#define SOS 0xda
#define EOI 0xd9

int main(void) {
    char* file = malloc(0x1000000); 
    read(fileno(stdin), file, 0x1000000 - 1);

    printf("howdy\n!");

        setvbuf(stdout, NULL, _IONBF, 0);
        setvbuf(stderr, NULL, _IONBF, 0);

    int location = 0;

    // Consume header
    location += 2;

    // Loop over every segment until End Of Image segment
    while (file[location + 1] != EOI && location < 500) {
        unsigned char header_byte = file[location + 1];
        uint16_t size = 0x100 * file[location + 2] + file[location + 3];

        printf("loc %d\n", location);
        printf("header %x\n", header_byte);
        printf("header=com %d\n", header_byte == COM);
        printf("size %d\n", size);

        if (header_byte == COM) {
            printf("found a com with size %d\n", size);
            char *comment = malloc(size + 2);

            memcpy(comment, &file[location + 4], size - 2);
        }

        location += size + 2;
        if (header_byte == SOS) {
            printf("inside sos\n");
            while ((unsigned char)file[location] != 0xff) {
                location++;
            }
        } 
    }

    return 0;
}
