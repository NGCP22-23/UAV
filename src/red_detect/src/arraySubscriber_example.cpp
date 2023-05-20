#include <rclcpp/rclcpp.hpp>
#include <NodeTools.cpp>
#include <iostream>

template<typename T, std::size_t S>
std::string arrayToString(T (&arr)[S]){

  std::string str = "";
  for(unsigned int i = 0; i < S; i++){
    str += std::to_string(arr[i]);
    if(i != S)
      str += ",";
  }

  return str;

}

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
 
  int data_from_ros[6] = {0,0,0,0,0,0};
  auto thresholdsubscriber = NodeTools::spawnThresholdSubscriber("threshold_sub", "thresholds");

  while(rclcpp::ok()){

    for(int i = 0; i < 6; i++)
      data_from_ros[i] = thresholdsubscriber->threshold_data[i];
    
    rclcpp::spin_some(thresholdsubscriber);

    std::cout << "Localized data: " << arrayToString(data_from_ros) << std::endl;



  }

  rclcpp::shutdown();

  return 0;

}