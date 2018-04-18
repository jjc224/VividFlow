//Inputs:
//1: Integer - Threshold. 1 is a good value
//2: "AnyDataType" - Image. Must be any data type due to issue on front end
//Outputs:
//1: Image - The output image.

#include "opencv2/core/utility.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"

#include <stdio.h>
#include <iostream>
#include <vividflow.h>

using namespace cv;
using namespace std;

int edgeThresh = 1;
Mat image, gray, edge, cedge;

int main( int argc, char** argv )
{
    int in_thresh = 0;
    string in_filename = "";
    string out_filename = "";

    initInterface(argc, argv);

    //input socket 1 - edge threshold
    in_thresh = readInteger(1);
    //input socket 2 - image file
    if(getInputSocketFilename(2) != NULL)
    {
        in_filename = getInputSocketFilename(2);
    }
    if(getInputSocketFilename(1) != NULL)
    {
        out_filename = getOutputSocketFilename(1);
    }

    cout << "In threshold = " << in_thresh << endl;
    cout << "in filename = " << in_filename << endl;
    cout << "out filename = " << out_filename << endl;

    edgeThresh = in_thresh;

    image = imread(in_filename, 1);
    if(image.empty())
    {
        printf("Cannot read image file: %s\n", in_filename.c_str());
        return -1;
    }
    cedge.create(image.size(), image.type());
    cvtColor(image, gray, COLOR_BGR2GRAY);

    //do edge detection
    //image.copyTo(cedge, edge);
    blur(gray, edge, Size(3,3));

    // Run the edge detector on grayscale
    Canny(edge, edge, edgeThresh, edgeThresh*3, 3);
    cedge = Scalar::all(0);

    imwrite( out_filename, edge );

    freeInterface();

    return 0;
}
