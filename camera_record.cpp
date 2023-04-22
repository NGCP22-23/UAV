#include <opencv2/opencv.hpp>

int main(){
    cv::VideoCapture cap(0); // 0 for the default camera, change the number if you have multiple cameras


    if (!cap.isOpened()) {
        std::cout << "Error: could not access the camera!" << std::endl;
        return -1;
    }

    while (true) {
        cv::Mat frame;
        cap >> frame; // capture a frame from the camera

        cv::imshow("Camera Feed", frame); // display the frame

        char key = cv::waitKey(1); // wait for a key to be pressed for 1ms

        if (key == 27) { // if the 'Esc' key is pressed, exit the loop
            break;
        }
    }

    cap.release(); // release the VideoCapture object
    cv::destroyAllWindows(); // destroy all the windows
    cv::namedWindow("Camera Feed", cv::WINDOW_NORMAL);
    cv::resizeWindow("Camera Feed", 640, 480); // optional, resize the window

}
