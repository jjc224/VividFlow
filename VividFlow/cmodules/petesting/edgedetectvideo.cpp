//Inputs:
//1: Integer - Threshold. 1 is a good value
//2: Video - Video.
//Outputs:
//1: Video - The output video.

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
#include "opencv2/core/utility.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"


#include <iostream>
#include <stdio.h>
#include <vividflow.h>

using namespace cv;
using namespace std;

//hide the local functions in an anon namespace
namespace
{
    Mat edge_detect_frame(Mat& frame, int edgeThresh)
    {
        Mat gray, edge, dst;
        cvtColor(frame, gray, COLOR_BGR2GRAY);

        blur( gray, edge, Size(3,3) );
        dst.create( frame.size(), frame.type() );

        // Run the edge detector on grayscale
        Canny(edge, edge, edgeThresh, edgeThresh*3, 3);
        dst = Scalar::all(0);

        frame.copyTo( dst, edge);

        return dst;
    }

    int edge_detect_video(std::string in_filename, std::string out_filename, int threshold)
    {
        VideoCapture capture(in_filename);
        int n = 0;
        Mat frame;

        bool bFramesLeftToProcess = true;

        int ex = static_cast<int>(capture.get(CV_CAP_PROP_FOURCC));     // Get Codec Type- Int form

       // Transform from int to char via Bitwise operators
       char EXT[] = {(char)(ex & 0XFF) , (char)((ex & 0XFF00) >> 8),(char)((ex & 0XFF0000) >> 16),(char)((ex & 0XFF000000) >> 24), 0};

       Size S = Size((int) capture.get(CV_CAP_PROP_FRAME_WIDTH),    // Acquire input size
                     (int) capture.get(CV_CAP_PROP_FRAME_HEIGHT));

       VideoWriter outputVideo;                                        // Open the output
       outputVideo.open(out_filename, ex, capture.get(CV_CAP_PROP_FPS), S, true);

       if (!outputVideo.isOpened())
       {
           cout  << "Could not open the output video for write: " << out_filename << endl;
           return -1;
       }

        while(bFramesLeftToProcess)
        {
            capture >> frame;
            if (frame.empty() == true)
            {
                bFramesLeftToProcess = false;
            }
            else
            {
                //outputVideo.write(res); //save or
                outputVideo << edge_detect_frame(frame, threshold);
            }
        }
        return 0;
    }
}

int main(int argc, char* argv[])
{
    int edgeThresh = 0;
    string in_filename = "";
    string out_filename = "";

    initInterface(argc, argv);

    //input socket 1 - edge threshold
    edgeThresh = readInteger(1);
    //input socket 2 - image file
    if(getInputSocketFilename(2) != NULL)
    {
        in_filename = getInputSocketFilename(2);
    }
    if(getInputSocketFilename(1) != NULL)
    {
        out_filename = getOutputSocketFilename(1);
    }

    cout << "frame to capture = " << edgeThresh << endl;
    cout << "in filename = " << in_filename << endl;
    cout << "out filename = " << out_filename << endl;

    //process(capture);
    edge_detect_video(in_filename, out_filename, edgeThresh);

    freeInterface();
    return 0;
}
