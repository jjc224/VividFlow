#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <stdarg.h>

#ifndef MODULE_H
#define MODULE_H

#define MAX_STRING_SIZE 256

struct IOInterface
{
	int inputID;     // Identifies input element in pipeline/chain.
	int outputID;    // Identifies output element in pipeline/chain.

	char *inputFile;
	char *outputFile;
};

struct ModuleInterface
{
	struct IOInterface *ioArguments;
	int numOfArgs;
};

struct GenericData
{
	int   size;
	void *buffer;
};

// Type declarations.
enum outputType
{
	OT_UNSUPPORTED,

	// Non-generic types of data.
	OT_STRING,
	OT_INT,
	OT_FLOAT,

	// Generic types of data (use binary I/O).
	OT_TEXTFILE,
	OT_IMAGEFILE,
	OT_VIDEOFILE,
	OT_ANY
};

struct OutputData
{
	union
	{
		struct GenericData *generic;
		char *string;
		int integer;
		double floatingPoint;
	} options;

	enum outputType type;
};

// Interface may as well be global.
// It's passed around a lot: will be easier for the module developer.
struct ModuleInterface *moduleInterface;

/**********************************************************************************************************************************************/

// Module interface function declarations.
// To be called at the beginning of each module.
struct ModuleInterface *initInterface(int argc, char *argv[]);

// Handles multiple IOInterfaces (i.e. a ModuleInterface).
// -------------------------------------------------------
void writeOutput(void);

// Handles single IOInterfaces.
// ----------------------------
void                writeNonGenericOutput(struct IOInterface *args, enum outputType type);
void                writeGenericOutput(struct IOInterface *args);
void                writeDataTypeOutput(struct IOInterface *args, struct OutputData *data);
struct GenericData *readGenericInput(struct IOInterface *args);

// Auxiliary "behind the scenes" function declarations.
// ----------------------------------------------------
void              *allocateMemory(size_t size);
void               freeInterface(void);
FILE              *openFile(const char *filename, const char *mode);
void               closeFile(FILE *file);
const char        *getFilenameExtension(const char *filename);
struct OutputData *getDataFromTextFile(const char *filename, enum outputType type);
enum outputType    getTypeFromFile(const char *filename);
void               outputFatalError(const char *format, ...);

// Functions for a module developer to utilise.
// --------------------------------------------
char               *getInputSocketFilename(int argument);
char               *getOutputSocketFilename(int argument);

struct GenericData *readGeneric(int argNum);
char               *readString(int argNum);
int                 readInteger(int argNum);
double              readFloat(int argNum);

void writeGeneric(int argNum, const struct GenericData *data);
void writeString(int argNum, const char *string);
void writeInteger(int argNum, const int number);
void writeFloat(int argNum, const double number);

/**********************************************************************************************************************************************/


// Module interface function definitions.
struct ModuleInterface *initInterface(int argc, char *argv[])
{
	moduleInterface = (ModuleInterface *) allocateMemory(sizeof (struct ModuleInterface));

	moduleInterface->numOfArgs   = (argc + 1);
	moduleInterface->ioArguments = (IOInterface *) allocateMemory(sizeof (struct IOInterface) * moduleInterface->numOfArgs);

	int option;

	while((option = getopt(argc, argv, "i:o:")) != -1)
	{
		int ioArgsIndex = 0;

		switch(option)
		{
			case 'i':
				ioArgsIndex = atoi(optarg) - 1;

				moduleInterface->ioArguments[ioArgsIndex].inputID   = atoi(optarg);
				moduleInterface->ioArguments[ioArgsIndex].inputFile = argv[optind++];    // Next argument after 'optarg'.
			break;

			case 'o':
				ioArgsIndex = atoi(optarg) - 1;

				moduleInterface->ioArguments[ioArgsIndex].outputID   = atoi(optarg);
				moduleInterface->ioArguments[ioArgsIndex].outputFile = argv[optind++];    // Next argument after 'optarg'.
			break;

			default:
				outputFatalError("option not supported.\n");
		}
	}

	return moduleInterface;
}

void writeOutput(void)
{
	if(moduleInterface == NULL)
		fprintf(stderr, "writeOutput(): ModuleInterface not initialised.");

	for(int i = 0; i < moduleInterface->numOfArgs; ++i)
	{
		enum outputType outFileType = getTypeFromFile(moduleInterface->ioArguments[i].outputFile);

		int isNotGenericData = (outFileType == OT_STRING || outFileType == OT_INT || outFileType == OT_FLOAT);

		if(isNotGenericData)
			writeNonGenericOutput(&moduleInterface->ioArguments[i], outFileType);
		else
			writeGenericOutput(&moduleInterface->ioArguments[i]);
	}
}

void writeNonGenericOutput(struct IOInterface *args, enum outputType type)
{
	FILE *outputFile        = openFile(args->outputFile, "w");
	struct OutputData *data = getDataFromTextFile(args->inputFile, type);

	switch(data->type)
	{
		case OT_STRING:  fprintf(outputFile, "%s\n",  data->options.string);         break;
		case OT_INT:     fprintf(outputFile, "%d\n",  data->options.integer);        break;
		case OT_FLOAT:   fprintf(outputFile, "%lf\n", data->options.floatingPoint);  break;

		default:
			fprintf(stderr, "writeNonGenericOutput(): data type not supported.");
	}

	closeFile(outputFile);
}

void writeGenericOutput(struct IOInterface *args)
{
	struct GenericData *data = readGenericInput(args);
	FILE *outputFile         = openFile(args->outputFile, "wb");

	fwrite(data->buffer, 1, data->size, outputFile);

	if(ferror(outputFile))
		fprintf(stderr, "Unable to write to file '%s'.\n", args->outputFile);

	closeFile(outputFile);
}

void writeDataTypeOutput(struct IOInterface *args, struct OutputData *data)
{
	FILE *outputFile = openFile(args->outputFile, "w");

	switch(data->type)
	{
		case OT_STRING:  fprintf(outputFile, "%s\n",  data->options.string);         break;
		case OT_INT:     fprintf(outputFile, "%d\n",  data->options.integer);        break;
		case OT_FLOAT:   fprintf(outputFile, "%lf\n", data->options.floatingPoint);  break;

		default:
			fprintf(stderr, "writeNonGenericOutput(): data type not supported.");
	}

	closeFile(outputFile);
}

struct GenericData *readGenericInput(struct IOInterface *args)
{
	if(args == NULL)
		fprintf(stderr, "readGenericInput(): IOInterface not initialised.");

	FILE *file = openFile(args->inputFile, "rb");
	int fileLength;

	fseek(file, 0, SEEK_END);
	fileLength = ftell(file);
	rewind(file);

	void *buffer = allocateMemory(sizeof (char) * (fileLength + 1));

	fread(buffer, fileLength, 1, file);
	closeFile(file);

	struct GenericData *fileData = (GenericData *) allocateMemory(sizeof (struct GenericData));

	fileData->size   = fileLength;
	fileData->buffer = buffer;

	return fileData;
}

// Auxiliary function definitions.
void *allocateMemory(size_t size)
{
	void *ptr;

	if((ptr = malloc(size)) == NULL)
	{
		fprintf(stderr, "allocateMemory(): unable to allocate memory.\n");
		exit(1);
	}

	return ptr;
}

void freeInterface(void)
{
	free(moduleInterface->ioArguments);
	free(moduleInterface);
}

FILE *openFile(const char *filename, const char *mode)
{
	FILE *file = fopen(filename, mode);

	if(file == NULL)
		fprintf(stderr, "Unable to open file '%s'\n", filename);

	return file;
}

void closeFile(FILE *file)
{
	if(fclose(file) == EOF)
		fprintf(stderr, "closeFile(): unable to close file.\n");
}

const char *getFilenameExtension(const char *filename)
{
	const char *dotPos = strrchr(filename, '.');

	if(dotPos == NULL || dotPos == filename)
		return "";

	return dotPos + 1;
}

struct OutputData *getDataFromTextFile(const char *filename, enum outputType type)
{
	struct OutputData *data = (OutputData *) allocateMemory(sizeof (struct OutputData));
	FILE *file              = openFile(filename, "r");

	switch(type)
	{
		case OT_STRING:
		{
			data->options.string = (char *) allocateMemory(sizeof (char) * MAX_STRING_SIZE);
			fgets(data->options.string, MAX_STRING_SIZE, file);

			size_t spanned                = strcspn(data->options.string, "\r\n");
			data->options.string[spanned] = '\0';    // Replaces newline with a null-byte. Handles LF, CF, CRLF, LFCR.

			break;
		}

		case OT_INT:     fscanf(file, "%d",  data->options.integer);        break;
		case OT_FLOAT:   fscanf(file, "%lf", data->options.floatingPoint);  break;

		default:
			fprintf(stderr, "getDataFromTextFile(): data type not supported.");
	}

	data->type = type;
	closeFile(file);

	return data;
}

enum outputType getTypeFromFile(const char *filename)
{
	const char *outputFileExt   = getFilenameExtension(filename);
	enum outputType outFileType = OT_UNSUPPORTED;

	if(strcmp(outputFileExt, "vfunsupported") == 0)
		outFileType = OT_UNSUPPORTED;
	else if(strcmp(outputFileExt, "vfstring") == 0)
		outFileType = OT_STRING;
	else if(strcmp(outputFileExt, "vfint") == 0)
		outFileType = OT_INT;
	else if(strcmp(outputFileExt, "vffloat") == 0)
		outFileType = OT_FLOAT;
	else if(strcmp(outputFileExt, "vftxt") == 0)
		outFileType = OT_TEXTFILE;
	else if(strcmp(outputFileExt, "vfimg") == 0)
		outFileType = OT_IMAGEFILE;
	else if(strcmp(outputFileExt, "vfvideo") == 0)
		outFileType = OT_VIDEOFILE;
	else if(strcmp(outputFileExt, "vfany") == 0)
		outFileType = OT_ANY;

	return outFileType;
}

char *getInputSocketFilename(int argument)
{
    return (argument <= moduleInterface->numOfArgs) ? moduleInterface->ioArguments[argument - 1].inputFile : NULL;
}

char *getOutputSocketFilename(int argument)
{
    return (argument <= moduleInterface->numOfArgs) ? moduleInterface->ioArguments[argument - 1].outputFile : NULL;
}

struct GenericData *readGeneric(int argNum)
{
	struct GenericData *data = readGenericInput(&moduleInterface->ioArguments[argNum - 1]);
	return data;
}

char *readString(int argNum)
{
	struct OutputData *data = getDataFromTextFile(moduleInterface->ioArguments[argNum - 1].inputFile, OT_STRING);
	return data->options.string;
}

int readInteger(int argNum)
{
	struct OutputData *data = getDataFromTextFile(moduleInterface->ioArguments[argNum - 1].inputFile, OT_INT);
	return data->options.integer;
}

double readFloat(int argNum)
{
	struct OutputData *data = getDataFromTextFile(moduleInterface->ioArguments[argNum - 1].inputFile, OT_FLOAT);
	return data->options.floatingPoint;
}

void writeString(int argNum, const char *string)
{
	struct OutputData data;

	data.type           = OT_STRING;
	data.options.string = (char *) allocateMemory(strlen(string + 1));
	strcpy(data.options.string, string);

	writeDataTypeOutput(&moduleInterface->ioArguments[argNum - 1], &data);

	free(data.options.string);
}

void writeGeneric(int argNum, const struct GenericData *data)
{
	writeGenericOutput(&moduleInterface->ioArguments[argNum - 1]);
}

void writeInteger(int argNum, const int number)
{
	struct OutputData data;

	data.type = OT_INT;
	data.options.integer = number;

	writeDataTypeOutput(&moduleInterface->ioArguments[argNum - 1], &data);
}

void writeFloat(int argNum, const double number)
{
	struct OutputData data;

	data.type = OT_FLOAT;
	data.options.floatingPoint = number;

	writeDataTypeOutput(&moduleInterface->ioArguments[argNum - 1], &data);
}

void outputFatalError(const char *format, ...)
{
	va_list args;

	va_start(args, format);

	fprintf(stderr, "Fatal error: ");
	vfprintf(stderr, format, args);

	va_end(args);
	// exit(1); 
}

#endif
