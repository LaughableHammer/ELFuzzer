#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "../libxml/xml.h"

void recurse(struct xml_element *node) {
	printf(node->key);
	printf("\n");
	
	if (node->first_child != NULL) {
		recurse(node->first_child);
	}
	
	if (node->next != NULL) {
		recurse(node->next);
	}
}


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

		recurse(st.root);
	}
	
	xml_free(st.root);

	return 0;
}