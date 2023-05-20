
//    _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _
// ,-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)
// `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-'
// 		       __      __  __  ______  __  __
// 	 (•̀ᴗ•́)و /\ \    /\ \/\ \/\  ___\/\ \_\ \    (◍＞◡＜◍)
// 	 ᶘ ◕ᴥ◕ᶅ	 \ \ \___\ \ \_\ \ \___  \ \  __ \  【≽ܫ≼】
//  (ﾟ◥益◤ﾟ)  \ \_____\ \_____\/\_____\ \_\ \_\  (ʘ言ʘ╬)
// 	 ᕙ(⇀‸↼‶)ᕗ \/_____/\/_____/\/_____/\/_/\/_/  (◕‿◕✿)
//    _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _
// ,-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)
// `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-'

// A simple client library to interact with ROS2 node functionality without a lot of the mess.

#include <chrono>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "std_msgs/msg/int32_multi_array.hpp"

using std::placeholders::_1;

namespace NodeTools
{

  std::string int32ArrayToString(std_msgs::msg::Int32MultiArray a, int sz){ // FOR LOGGING PURPOSES ONLY!!! sz = sizeof(array) / sizeof(type)

    int i;
    std::string s = "";
    for (i = 0; i < sz; i++){
      s = s + std::to_string(a.data[i]);
      if(i != 5)
        s = s + ",";
    }
    
    return s;
  }

  class Subscriber : public rclcpp::Node // Versatile ROS2 based Subscriber class with built-in callback (ROS console output). Constructor has two string parameters: [1] the subscribers name [2] the name of the desired topic
  {

  public:
    
    Subscriber(std::string name, std::string topic);

  private:

    void topic_callback(const std_msgs::msg::String::SharedPtr msg) const;
    //deposit the msg data into something in the class

    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;

  };

  auto spawnSubscriber(std::string name, std::string topic){

    return std::make_shared<NodeTools::Subscriber>(name, topic);

  }

  class nPublisher : public rclcpp::Node 
  {

    public:

      nPublisher(std::string name, int outputBuffer);

      // void update the publisher's message
    
    private:

      void timer_callback();
      
      std::string message = "hello world";
      rclcpp::TimerBase::SharedPtr timer_;
      rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;

  };

  auto spawnPublisher(std::string name, int outputBuffer = 10){

    return std::make_shared<NodeTools::nPublisher>(name, outputBuffer);

  }
 
  class ThresholdPublisher : public rclcpp::Node
  {

    public:

        ThresholdPublisher(std::string name, int outputBuffer);
        void export_data(int (&data)[6]);

    private:

        void timer_callback();

        int d[6];

        rclcpp::TimerBase::SharedPtr timer_;
        rclcpp::Publisher<std_msgs::msg::Int32MultiArray>::SharedPtr publisher_;

  };

  auto spawnThresholdPublisher(std::string name, int outputBuffer = 100){

    return std::make_shared<NodeTools::ThresholdPublisher>(name, outputBuffer);

  }

  class ThresholdSubscriber : public rclcpp::Node // Versatile ROS2 based Subscriber class with built-in callback (ROS console output). Constructor has two string parameters: [1] the subscribers name [2] the name of the desired topic
  {

  public:
    
    ThresholdSubscriber(std::string name, std::string topic);
    
    int threshold_data[6];

  private: 

    void topic_callback(const std_msgs::msg::Int32MultiArray::SharedPtr data);
    void import_data(std_msgs::msg::Int32MultiArray data);
    //deposit the msg data into something in the class

    rclcpp::Subscription<std_msgs::msg::Int32MultiArray>::SharedPtr subscription_;
    

  };

  auto spawnThresholdSubscriber(std::string name, std::string topic){

    return std::make_shared<NodeTools::ThresholdSubscriber>(name, topic);

  }

}