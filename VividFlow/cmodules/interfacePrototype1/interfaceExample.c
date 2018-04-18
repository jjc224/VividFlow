#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include "module.h"

void printModuleInterface(struct ModuleInterface *interface);    // Mostly for debugging.

int main(int argc, char *argv[])
{
	struct ModuleInterface args;
	int option;

	while((option = getopt(argc, argv, "i:o:")) != -1)
	{
		switch(option)
		{
			case 'i':
				args.inputID   = atoi(optarg);
				args.inputFile = argv[optind++];    // Next argument after 'optarg'.
			break;

			case 'o':
				args.outputID   = atoi(optarg);
				args.outputFile = argv[optind++];    // Next argument after 'optarg'.

				writeOutput(&args, 0, OT_TEXTFILE);
			break;

			default:
				fprintf(stderr, "Option '%c' not supported.\n", option);
				exit(1);
		}
	}

	return 0;
}

void printModuleInterface(struct ModuleInterface *interface)
{
	printf("Input ID: %d\n", interface->inputID);
	printf("Input file: %s\n\n", interface->inputFile);

	printf("Output ID: %d\n", interface->outputID);
	printf("Output file: %s\n", interface->outputFile);
}
