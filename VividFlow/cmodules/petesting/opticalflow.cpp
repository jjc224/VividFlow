// Input sockets:
//	1. inputvid is of type Video.

// Output sockets:
//	1. outputvid is of type Video.

#include <opencv2/highgui/highgui.hpp>
#include "opencv2/imgproc.hpp"
#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/video/tracking.hpp"

#include <vividflow.h>
#include <string>

using namespace cv;

void calculateOpticalFlow( std::string in_filename, std::string out_filename );

int main(int argc, char *argv[])
{
    initInterface(argc, argv);

	// Input sockets:
    std::string in_file = getInputSocketFilename(1);
    std::string out_file = getOutputSocketFilename(1);

    calculateOpticalFlow(in_file, out_file);

    freeInterface();

    return 0;
}

void calculateOpticalFlow( std::string in_filename, std::string out_filename )
{
    VideoCapture cap(in_filename);

    Mat flow, frame;
    UMat  flowUmat, prevgray;


    int ex = static_cast<int>(cap.get(CV_CAP_PROP_FOURCC));     // Get Codec Type- Int form

   // Transform from int to char via Bitwise operators
   char EXT[] = {(char)(ex & 0XFF) , (char)((ex & 0XFF00) >> 8),(char)((ex & 0XFF0000) >> 16),(char)((ex & 0XFF000000) >> 24), 0};

   Size S = Size((int) cap.get(CV_CAP_PROP_FRAME_WIDTH),    // Acquire input size
                 (int) cap.get(CV_CAP_PROP_FRAME_HEIGHT));

    VideoWriter outputVideo;                                        // Open the output
    outputVideo.open(out_filename, ex, cap.get(CV_CAP_PROP_FPS), S, true);

   while( cap.grab() == true )
   {
            Mat img;
            Mat original;

           // get a frame from the video file
           cap.retrieve(img, CV_CAP_OPENNI_BGR_IMAGE);
           //resize(img, img, Size(640, 480));

           // save original for later
           img.copyTo(original);

           // make the current frame gray
           cvtColor(img, img, COLOR_BGR2GRAY);

           if (prevgray.empty() == false )
		   {
              // calculate optical flow
              calcOpticalFlowFarneback(prevgray, img, flowUmat, 0.4, 1, 12, 2, 8, 1.2, 0);
              // copy Umat container to standard Mat
              flowUmat.copyTo(flow);

               // By y += 5, x += 5 you can specify the grid
              for (int y = 0; y < original.rows; y += 10)
                 for (int x = 0; x < original.cols; x += 10)
                 {
                     // get the flow from y, x position * 10 for better visibility
                     const Point2f flowatxy = flow.at<Point2f>(y, x) * 10;
                     // draw line at flow direction
                     line(original, Point(x, y), Point(cvRound(x + flowatxy.x), cvRound(y + flowatxy.y)), Scalar(255,0,0));
                 }

              // draw the results
              //namedWindow("prew", WINDOW_AUTOSIZE);
              //imshow("prew", original);
              outputVideo << original;

              // fill previous image again
              img.copyTo(prevgray);
        }
        else
             // fill previous image in case prevgray.empty() == true
             img.copyTo(prevgray);
      int key1 = waitKey(2);
   }
   return;
 }
