//    _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _
// ,-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)
// `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-'
// 		     __      __  __  ______  __  __    
// 	 (•̀ᴗ•́)و /\ \    /\ \/\ \/\  ___\/\ \_\ \    (◍＞◡＜◍)
// 	 ᶘ ◕ᴥ◕ᶅ	 \ \ \___\ \ \_\ \ \___  \ \  __ \  【≽ܫ≼】
//  (ﾟ◥益◤ﾟ)  \ \_____\ \_____\/\_____\ \_\ \_\  (ʘ言ʘ╬)
// 	 ᕙ(⇀‸↼‶)ᕗ \/_____/\/_____/\/_____/\/_/\/_/  (◕‿◕✿)
//    _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _
// ,-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)
// `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-'

#include <NodeTools.hpp>

using namespace std::chrono_literals;

NodeTools::Subscriber::Subscriber(std::string name, std::string topic) : rclcpp::Node(name){

    subscription_ = this->create_subscription<std_msgs::msg::String>
    (
        topic, 10, std::bind(&NodeTools::Subscriber::topic_callback, this, _1)
    );

}

void NodeTools::Subscriber::topic_callback(const std_msgs::msg::String::SharedPtr msg) const{

    RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg->data.c_str());

}

NodeTools::nPublisher::nPublisher(std::string name,  int outputBuffer) : rclcpp::Node(name) {

    publisher_ = this->create_publisher<std_msgs::msg::String>(name, outputBuffer);
    timer_ = this->create_wall_timer(500ms, std::bind(&NodeTools::nPublisher::timer_callback, this));

}

void NodeTools::nPublisher::timer_callback() {

    auto packet = std_msgs::msg::String();

    packet.data = message;

    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", packet.data.c_str());
    publisher_-> publish(packet);

}

NodeTools::ThresholdPublisher::ThresholdPublisher(std::string name, int outputBuffer) : rclcpp::Node(name) {

  publisher_ = this->create_publisher<std_msgs::msg::Int32MultiArray>(name, outputBuffer);
  timer_ = this->create_wall_timer(500ms, std::bind(&NodeTools::ThresholdPublisher::timer_callback, this));

}

void NodeTools::ThresholdPublisher::timer_callback() {

    auto packet = std_msgs::msg::Int32MultiArray();

    packet.data = {d[0], d[1], d[2], d[3], d[4], d[5]};

    RCLCPP_INFO(this->get_logger(), "Publishing array");
    publisher_->publish(packet);

}

void NodeTools::ThresholdPublisher::export_data(int (&data)[6]){

    for(int i = 0; i < 6; i++)
        d[i] = data[i];

}

NodeTools::ThresholdSubscriber::ThresholdSubscriber(std::string name, std::string topic) : rclcpp::Node(name){

    subscription_ = this->create_subscription<std_msgs::msg::Int32MultiArray>
    (
        topic, 10, std::bind(&NodeTools::ThresholdSubscriber::topic_callback, this, _1)
    );

}

void NodeTools::ThresholdSubscriber::topic_callback(const std_msgs::msg::Int32MultiArray::SharedPtr data) {

    RCLCPP_INFO(this->get_logger(), "data recieved: '%s'", NodeTools::int32ArrayToString(*data, 6).c_str());
    import_data(*data);

}

void NodeTools::ThresholdSubscriber::import_data(std_msgs::msg::Int32MultiArray d) {

    for(int i = 0; i < 5; i++)
        threshold_data[i] = d.data[i];

}