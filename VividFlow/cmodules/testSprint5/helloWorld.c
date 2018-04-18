#include <stdio.h>
#include "../interfaceSprint2/module.h"

const char *g_Message = "Hello world.";

const char *helloWorld(void)
{
	printf("%s", g_Message);
	return g_Message;
}

int main(int argc, char *argv[])
{
	initInterface(argc, argv);

	const char *message = helloWorld();
	writeString(1, message);

	freeInterface();

	return 0;
}

