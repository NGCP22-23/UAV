#include <rclcpp/rclcpp.hpp>
#include <NodeTools.cpp>
#include <stdlib.h>
#include <iostream>
#include <time.h>

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
 
  srand(time(NULL));

  int data[6] = {0,1,2,3,4,5}; // init live values
  int buffer = 100; // mem buffer

  auto thresholdpublisher = NodeTools::spawnThresholdPublisher("thresholds", buffer);

  while(rclcpp::ok()){

    thresholdpublisher->export_data(data); // refresh publisher values
    rclcpp::spin_some(thresholdpublisher); // send publisher to thread

    for(int i = 0; i < 6; i++)
      data[i] = rand() % 255 + 1;

  }

  rclcpp::shutdown();

  return 0;
}