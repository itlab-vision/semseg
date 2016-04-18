#include "opencv2/highgui/highgui.hpp"
#include <stdio.h>
#include <iostream>

using namespace cv;
using namespace std;

int main(int argc, char* argv[]) {
    VideoCapture cap(argv[1]);

    if (!cap.isOpened()) {
         cout << "Cannot open the video file" << endl;
         return -1;
    }

    double Hz = atof(argv[2]);

    double fps = cap.get(CV_CAP_PROP_FPS);
    cout << "Frame per seconds : " << fps << endl;

    int skip_frames = (int)(fps / Hz + 0.5) - 1;
    if (skip_frames < 1) {
        skip_frames = 0;
    }

    cout << "Number skipped frames : " << skip_frames << endl;

    for (int i = 0; ; i++) {
        Mat frame;

        bool bSuccess = cap.read(frame);
        if (!bSuccess) {
            cout << "Cannot read the frame from video file" << endl;
            break;
        }

        char filename[18];
        int cx;

        cx = snprintf (filename, 18, "./frames/%04d.png", i);
        if (cx < 0) {
            cout << "Cannot create filename " << i << endl;
            return -1;
        }
        bool wsuccess = imwrite(filename, frame);
        if (!wsuccess) {
            cout << "Cannot write frame" << endl;
        }

        waitKey(0);
        for (int j = 0; j < skip_frames; j++) {
            bSuccess = cap.read(frame);
            if (!bSuccess) {
                break;
            }
        }
    }

    return 0;
}