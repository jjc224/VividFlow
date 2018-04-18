#include <stdio.h>
#include <stdlib.h>
#include "module.h"
 
// Usage example: ./a.out -i1 test2.vfimg -o1 out2.vfimg
 
int main(int argc, char *argv[])
{
	initInterface(argc, argv);
	
	struct GenericData *data = readGeneric(1);
	writeGeneric(1, data);

	free(data->buffer);
	free(data);

	freeInterface();
	return 0;
}
