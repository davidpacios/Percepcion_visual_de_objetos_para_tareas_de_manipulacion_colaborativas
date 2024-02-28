/**
 * Basic example of a service provider (server)
 * Authors: Laurent Lequièvre, Juan Antonio Corrales
 * Institution: Institut Pascal, Clermont-Ferrand, France
 */
 
 /**
 * Common libraries of ROS for having access to roscpp functionalities
 */
#include "ros/ros.h"
/**
 * Automatically generated header for service 'AddTwoInts' of package 'tutorials'
 */
#include "tutorials/AddTwoInts.h"

/**
 * Callback function that is invoked to treat the service. It receives as input the request coming from the client
 * and it should generate as output the response that will be sent back to the client.
 * When ros::spin() is used, the callback is invoked as soon as possible when one service request is received.
 * When ros::spinOnce() is used, callbacks of requests accumulated after the previous spinOnce() are invoked.
 */
bool add(tutorials::AddTwoInts::Request  &req,
         tutorials::AddTwoInts::Response &res)
{
  res.sum = req.a + req.b;
  ROS_INFO("request: x=%ld, y=%ld", (long int)req.a, (long int)req.b);
  ROS_INFO("sending back response: [%ld]", (long int)res.sum);
  return true;
}

int main(int argc, char **argv)
{
  /** 
   * Initialization of a ROS node with name 'add_two_ints_server', 
   * giving acces to line command arguments (argc, argv). The name of the node should be unique.
   */
  ros::init(argc, argv, "add_two_ints_server");
   /**
   * Creation of handle for accessing the node. The first handle starts the node
   * (equivalent to ros::start()) and the destruction of the last handle finishes
   * the node (equivalent to ros::shutdown()).
   */
  ros::NodeHandle n;

  /**
   * Advertisement of the service 'add_two_ints' to the master so that it can be used by other nodes. 
   * This method will return a 'ros::ServiceServer' object for having access to the service.
   * When all the instances of a ServiceServer are destroyed, the service is unadvertised and callback is stopped.
   */
  ros::ServiceServer service = n.advertiseService("add_two_ints", add);
  ROS_INFO("Ready to add two ints.");
  
  /**
   * ros::spin() generates an infinite loop that automatically invoke callbacks when
   * messages are received through the topic. This loop ends int he same conditions when
   * ros::ok() returns false.
   */
  ros::spin();

  return 0;
}
