#include <stdio.h>
#include <stdlib.h>
#include "module.h"

// Usage example: ./a.out -i1 test.vfstring -o1 out.vfstring -i2 out.vfstring -o2 out2.vfstring

char *concatStrings(const char *one, const char *two)
{
	size_t length      = strlen(one) + strlen(two);
	char *outputString = allocateMemory(sizeof(char) * length + 1);

	strcpy(outputString, one);
	strcat(outputString, two);

	outputString[length] = '\0';
	return outputString;
}

int main(int argc, char *argv[])
{
	initInterface(argc, argv);

	char *stringOne = readString(1);
	char *stringTwo = readString(2);
	char *oneAndTwo = concatStrings(stringOne, stringTwo);

	writeString(2, oneAndTwo);

	freeInterface();
	return 0;
}
