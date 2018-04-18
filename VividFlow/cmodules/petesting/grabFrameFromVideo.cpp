//Inputs:
//1: Integer - Frame Index, the index number of the frame to grab
//2: Video - Source Video
//Outputs:
//1: Image - The output image.

//Video test module adapted by Philip Edwards from:
/*
* starter_video.cpp
*
*  Created on: Nov 23, 2010
*      Author: Ethan Rublee
*
*  Modified on: April 17, 2013
*      Author: Kevin Hughes
*
* A starter sample for using OpenCV VideoCapture with capture devices, video files or image sequences
* easy as CV_PI right?
*/

#include <opencv2/imgcodecs.hpp>
#include <opencv2/videoio/videoio.hpp>
#include <opencv2/highgui/highgui.hpp>

#include <iostream>
#include <stdio.h>
#include <vividflow.h>

using namespace cv;
using namespace std;

//hide the local functions in an anon namespace
namespace
{
    int get_frame(std::string in_filename, std::string out_filename, int frameToCap)
    {
        VideoCapture capture(in_filename);
        int n = 0;
        Mat frame;

        for (int i = 0; i < frameToCap; i++)
        {
            capture >> frame;
            if (frame.empty())
            {
                return -1;
            }
        }
        imwrite( out_filename, frame );
        return 0;
    }
}

int main(int argc, char* argv[])
{
    int frameIdx = 0;
    string in_filename = "";
    string out_filename = "";

    initInterface(argc, argv);

    //input socket 1 - edge threshold
    frameIdx = readInteger(1);
    //input socket 2 - image file
    if(getInputSocketFilename(2) != NULL)
    {
        in_filename = getInputSocketFilename(2);
    }
    if(getInputSocketFilename(1) != NULL)
    {
        out_filename = getOutputSocketFilename(1);
    }

    cout << "frame to capture = " << frameIdx << endl;
    cout << "in filename = " << in_filename << endl;
    cout << "out filename = " << out_filename << endl;

    //process(capture);
    get_frame(in_filename, out_filename, frameIdx);

    freeInterface();
    return 0;
}
