#include <stdio.h>
#include <stdlib.h>
#include "module.h"

// Usage example: ./a.out -i1 test.vfstring -o1 out.vfstring

char *revString(const char *string)
{
	int stringLen      = strlen(string);
	char *outputString = allocateMemory(sizeof(char) * stringLen);

	for(int i = 0; i < stringLen; ++i)
		outputString[i] = string[stringLen - i - 1];

	outputString[stringLen] = '\0';
	return outputString;
}

int main(int argc, char *argv[])
{
	struct ModuleInterface *interface = initInterface(argc, argv);

	char *testString    = readString(interface, 1);
	char *revTestString = revString(testString);

	writeString(interface, 1, revTestString);

	freeInterface(interface);

	return 0;
}

