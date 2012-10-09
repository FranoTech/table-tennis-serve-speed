
/*
A simple example of object tracking using thresholding. Takes live video
from webcam and draws a line where it sees the image. The threshold image
can also be seen.

Press spacebar to clear yellow line. Esc to exit. 
Slide bars can be moved to accurately determine the best min and max values.

Compile on Ubuntu 12.04:
g++ `pkg-config opencv --cflags` opencv-balltrack.cpp -o balltrack `pkg-config --libs opencv`

Run:
./balltrack

*/

//set the camera resolution grab is CUST_RES set to 1
#define CUST_RES 1
#define RES_H 640
#define RES_V 480

#include "stdio.h"
#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"

IplImage* GetThresholdedImage(IplImage* img, int h_min, int s_min, int v_min, int h_max, int s_max, int v_max)
{
	// Convert the image into an HSV image
    IplImage* imgHSV = cvCreateImage(cvGetSize(img), 8, 3);
    cvCvtColor(img, imgHSV, CV_BGR2HSV);
    IplImage* imgThreshed = cvCreateImage(cvGetSize(img), 8, 1);
	//get rid of all colours not in range low-upper bound
    cvInRangeS(imgHSV, cvScalar(h_min, s_min, v_min), cvScalar(h_max, s_max, v_max), imgThreshed);
    cvReleaseImage(&imgHSV);
    return imgThreshed;
}

int main()
{
    int h_min =0;
    int s_min =0;
    int v_min =0;
    int h_max =180;
    int s_max =255;
    int v_max =255;
	// Initialize capturing live feed from the camera
    CvCapture* capture = 0;
    capture = cvCaptureFromCAM(0);

    // Couldn't get a device? Throw an error and quit
    if(!capture)
    {
        printf("Could not initialize capturing...\n");
        return -1;
    }

    //if CUST_RES set to 1 then set resolution, otherwise use default
    if(CUST_RES)
    {
        cvSetCaptureProperty(capture,CV_CAP_PROP_FRAME_WIDTH,RES_H);
        cvSetCaptureProperty(capture,CV_CAP_PROP_FRAME_HEIGHT,RES_V);
    }
	
	// The two windows we'll be using
    cvNamedWindow("video");
    cvNamedWindow("thresh");
    cvNamedWindow("variables");
       //create trackbars so that we can test colour ranges faster
    cvCreateTrackbar("hue_min", "variables", &h_min, 180, NULL);
    cvCreateTrackbar("saturation_min", "variables", &s_min, 255, NULL);
    cvCreateTrackbar("value_min","variables",&v_min,255,NULL);
    cvCreateTrackbar("hue_max", "variables", &h_max, 180, NULL);
    cvCreateTrackbar("saturation_max", "variables", &s_max, 255, NULL);
    cvCreateTrackbar("value_max","variables",&v_max,255,NULL);
	
	// This image holds the "scribble" data...
    // the tracked positions of the ball
    IplImage* imgScribble = NULL;
	
	// An infinite loop
    while(true)
    {
        // Will hold a frame captured from the camera
        IplImage* frame = 0;
        frame = cvQueryFrame(capture);
		// If we couldn't grab a frame... quit
        if(!frame)
            break;
		// If this is the first frame, we need to initialize it
        if(imgScribble == NULL)
        {
            imgScribble = cvCreateImage(cvGetSize(frame), 8, 3);
        }
		
		// Holds the yellow thresholded image (yellow = white, rest = black)
        IplImage* imgYellowThresh = GetThresholdedImage(frame, h_min, s_min, v_min, h_max, s_max, v_max);
		
		// Calculate the moments to estimate the position of the ball
        CvMoments *moments = (CvMoments*)malloc(sizeof(CvMoments));
        cvMoments(imgYellowThresh, moments, 1);
 
        // The actual moment values
        double moment10 = cvGetSpatialMoment(moments, 1, 0);
        double moment01 = cvGetSpatialMoment(moments, 0, 1);
        double area = cvGetCentralMoment(moments, 0, 0);
		
		// Holding the last and current ball positions
        static int posX = 0;
        static int posY = 0;
 
        int lastX = posX;
        int lastY = posY;
 
        posX = moment10/area;
        posY = moment01/area;
		
		// Print it out for debugging purposes
        printf("position (%d,%d)\n", posX, posY);
		
		// We want to draw a line only if its a valid position
        if(lastX>0 && lastY>0 && posX>0 && posY>0)
        {
            // Draw a yellow line from the previous point to the current point
            cvLine(imgScribble, cvPoint(posX, posY), cvPoint(lastX, lastY), cvScalar(0,255,255), 5);
        }
		// Add the scribbling image and the frame...
        cvAdd(frame, imgScribble, frame);
        cvShowImage("thresh", imgYellowThresh);
        cvShowImage("video", frame);
		// Wait for a keypress
        
	int c = cvWaitKey(10);
        if(c!=-1)
        {
	    if(c==27)
	    {
            	// If esc char pressed, break out of the loop
            	break;
            }
            if(c=32)
            {
                //If space bar pressed, clear line from image
                imgScribble = cvCreateImage(cvGetSize(frame), 8, 3);
            }
        }
		
		// Release the thresholded image+moments... we need no memory leaks.. please
        cvReleaseImage(&imgYellowThresh);
        delete moments;
    }
	
	// We're done using the camera. Other applications can now use it
    cvReleaseCapture(&capture);
    return 0;
}



