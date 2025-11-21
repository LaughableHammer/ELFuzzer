#include <stdio.h>
#include <fcntl.h>
#include <libelf.h>
#include <gelf.h>
#include <elfutils/libdwfl.h>
#include <stdlib.h>
#include <unistd.h>

int main(void) {
    char* file = malloc(0x100000); 
    read(fileno(stdin), file, 0x100000 - 1);

    if (elf_version(EV_CURRENT) == EV_NONE) {
        fprintf(stderr, "ELF library initialization failed\n");
        return 1;
    }

    Elf *elf = elf_memory(file, 0x100000);
    if (!elf) {
        fprintf(stderr, "elf_begin failed: %s\n", elf_errmsg(-1));
        return 1;
    }

    GElf_Ehdr ehdr;
    if (gelf_getehdr(elf, &ehdr) == NULL) {
        fprintf(stderr, "gelf_getehdr failed: %s\n", elf_errmsg(-1));
        return 1;
    }

    printf("Class: %s\n", ehdr.e_ident[EI_CLASS] == ELFCLASS64 ? "ELF64" : "ELF32");

    printf("Program Interpreter (PT_INTERP):\n");
    size_t nph;
    elf_getphdrnum(elf, &nph);
    for (size_t i = 0; i < nph; i++) {
        GElf_Phdr phdr;
        gelf_getphdr(elf, i, &phdr);

        if (phdr.p_type == PT_INTERP) {
            char *interp = elf_getdata_rawchunk(
                elf,
                phdr.p_offset,
                phdr.p_filesz,
                ELF_T_CHDR
            )->d_buf;

            printf(interp);
        }
    }

    return 0;
}
