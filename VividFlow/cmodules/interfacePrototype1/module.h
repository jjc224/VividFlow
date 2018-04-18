#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef MODULE_H
#define MODULE_H

// Type declarations.
struct ModuleInterface
{
	int inputID;     // Identifies input element in pipeline/chain.
	int outputID;    // Identifies output element in pipeline/chain.

	char *inputFile;
	char *outputFile;
};

struct FileData
{
	int size;
	void *buffer;
};

enum outputType
{
	OT_STRING,
	OT_INT,
	OT_TEXTFILE,
	OT_IMAGEFILE
};


/**********************************************************************************************************************************************/

// Module interface function declarations.
void writeOutput(struct ModuleInterface *args, int numOfInputs, enum outputType type);
struct FileData *readGenericInput(struct ModuleInterface *args, int numOfInputs);

// Modules.
// TODO: move to its own file. 
char *revString(char *string);

// Auxiliary function declarations.
FILE *openFile(char *filename, char *mode);
void closeFile(FILE *file);

/**********************************************************************************************************************************************/


// Module interface function definitions.
void writeOutput(struct ModuleInterface *args, int numOfInputs, enum outputType type)
{
	struct FileData *inputData = readGenericInput(args, numOfInputs);
	FILE *outputFile = openFile(args->outputFile, "wb");

	fwrite(inputData->buffer, 1, inputData->size, outputFile);

	if(ferror(outputFile))
	{
		fprintf(stderr, "Unable to write to file '%s'\n", args->outputFile);
		// Error handling within the chain?
	}

	closeFile(outputFile);
}

struct FileData *readGenericInput(struct ModuleInterface *args, int numOfInputs)
{
	FILE *file = openFile(args->inputFile, "rb");
	int fileLength;

	fseek(file, 0, SEEK_END);
	fileLength = ftell(file);
	rewind(file);

	void *buffer = malloc(sizeof(char) * (fileLength + 1));

	fread(buffer, fileLength, 1, file);
	closeFile(file);

	struct FileData *fileData = malloc(sizeof(struct FileData));
	
	fileData->size   = fileLength;
	fileData->buffer = buffer;

	return fileData;
}

char *revString(char *string)
{
	int stringLen      = strlen(string);
	char *outputString = malloc(sizeof(char) * stringLen);

	for(int i = 0; i < stringLen; ++i)
		outputString[i] = string[stringLen - i - 1];

	outputString[stringLen] = '\0';
	return outputString;
}

// Auxiliary function definitions.
FILE *openFile(char *filename, char *mode)
{
	FILE *file = fopen(filename, mode);

	if(file == NULL)
	{
		fprintf(stderr, "Unable to open file '%s'\n", filename);
		// Error handling within the chain?
	}

	return file;
}

void closeFile(FILE *file)
{
	fclose(file);
}

const char *getFilenameExtension(const char *filename)
{
	const char *dotPos = strrchr(filename, '.');

	if(!dotPos || dotPos == filename)
		return "";

	return dotPos + 1;
}

#endif
