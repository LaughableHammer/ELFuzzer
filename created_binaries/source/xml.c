#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "../libxml/xml.h"

int main(void) {
	struct xml_state st;

	memset(&st, 0, sizeof(st));

	while(1) {
		char buf[256];

		/* read from stdin */
		{
			size_t n = read(
				STDIN_FILENO,
				buf,
				sizeof(buf));

			if (n < 1) {
				break;
			}

			buf[n] = 0;
		}

		if (xml_parse_chunk(&st, buf)) {
			xml_free(st.root);
			fprintf(stderr, "error: parse error\n");
			return -1;
		}

		if (st.root) {
			struct xml_element *e;

			if ((e = xml_find(st.root, "hello/world"))) {
				printf("Tag found: %s\n", e->key);
				break;
			}
		}
	}

	xml_free(st.root);

	return 0;
}