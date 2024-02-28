/**
 * Basic example of a topic subscriber (reader from a topic)
 * Authors: Laurent Lequièvre, Juan Antonio Corrales
 * Institution: Institut Pascal, Clermont-Ferrand, France
 */

/**
 * Common libraries of ROS for having access to roscpp functionalities
 */
#include "ros/ros.h"
/**
 * Automatically generated header for message 'positionAngle' of package 'tutorials'
 */
#include "tutorials/positionAngle.h"

/**
 * Callback function that is invoked to treat each message received through the topic.
 * When ros::spin() is used, the callback is invoked as soon as possible when one message is received.
 * When ros::spinOnce() is used, callbacks of messages accumulated after the previous spinOnce() are invoked.
 * The message is passed as input parameter through a const shared pointer whose memory we do not need to manage.
 */
void positionCallback(const tutorials::positionAngle::ConstPtr& msg)
{
  ROS_INFO("I heard message %d: [%f, %f, %f]", msg->header.seq, msg->x, msg->y, msg->angle);
}


int main(int argc, char **argv)
{
  /** 
   * Initialization of a ROS node with name 'position_subscriber', 
   * giving acces to line command arguments (argc, argv). The name of the node should be unique.
   */
  ros::init(argc, argv, "position_subscriber");

  /**
   * Creation of handle for accessing the node. The first handle starts the node
   * (equivalent to ros::start()) and the destruction of the last handle finishes
   * the node (equivalent to ros::shutdown()).
   */
  ros::NodeHandle n;

  /**
   * Subscription to 'position' topic with an input buffer of 1000 messages.
   * The callback function 'positionCallback' will be called to treat each message
   * previously received from the topic and stored in the input buffer. 
   * The ros::Subscriber object returned by this method will be used to access to the
   * topic and when it will be destroyed, the subscription will be cancelled.
   */
  ros::Subscriber sub = n.subscribe("position", 1000, positionCallback);

  /**
   * ros::spin() generates an infinite loop that automatically invoke callbacks when
   * messages are received through the topic. This loop ends int he same conditions when
   * ros::ok() returns false.
   */
  ros::spin();


  return 0;
}
// %EndTag(FULLTEXT)%
