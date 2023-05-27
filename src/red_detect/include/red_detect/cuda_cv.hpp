#include <opencv2/opencv.hpp>
#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32.hpp"

#include <Diagnostics.cpp>

#include <chrono>
#include <iostream>
#include <math.h>
#include <string.h>

using namespace std::chrono_literals;

class errorPublisher : public rclcpp::Node {

    public:

        int dx, dy, dist;

        errorPublisher();
        virtual ~errorPublisher();

        void pubDist(int dx, int dy);

    private:

        rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr dx_publisher_;
        rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr dy_publisher_;
        rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr dist_publisher_;

        rclcpp::TimerBase::SharedPtr timer_;


};