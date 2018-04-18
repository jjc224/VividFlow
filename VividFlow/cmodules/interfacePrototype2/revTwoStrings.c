#include <stdio.h>
#include <stdlib.h>
#include "module.h"

// Usage example: ./a.out -i1 test.vfstring -o1 out.vfstring -i2 out.vfstring -o2 out2.vfstring

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
	initInterface(argc, argv);

	for(int argNum = 1; argNum <= 2; ++argNum)
	{
		char *testString    = readString(argNum);
		char *revTestString = revString(testString);

		writeString(argNum, revTestString);
	}

	freeInterface();
	return 0;
}
