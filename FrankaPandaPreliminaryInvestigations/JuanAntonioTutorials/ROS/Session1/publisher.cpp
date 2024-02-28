/**
 * Basic example of a topic publisher (writer on a topic)
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


int main(int argc, char **argv)
{
  /** 
   * Initialization of a ROS node with name 'position_publisher', 
   * giving acces to line command arguments (argc, argv). The name of the node should be unique.
   */
  ros::init(argc, argv, "position_publisher");

  /**
   * Creation of handle for accessing the node. The first handle starts the node
   * (equivalent to ros::start()) and the destruction of the last handle finishes
   * the node (equivalent to ros::shutdown()).
   */
  ros::NodeHandle n;

  /**
   * Advertisement of the topic 'position' to the master so that it can be subscribed by other nodes. 
   * This topic will transmit messages of type 'beginner_tutorials::positionAngle'.
   * The second parameter indicates the size of the output message buffer associated with the topic.
   * This method will return a 'ros::Publisher' object for having access to the topic
   * in order to send messages through it. When this object is destroyed, the topic will be unadvertised.
   */
  ros::Publisher pub = n.advertise<tutorials::positionAngle>("position", 1000);

  /**
   * Definition of the execution frequency (in Hz) of the main loop of the node
   */
  ros::Rate loop_rate(1);

  int angle=0, posX= 100, posY= 200, incrAngle= 5, iter= 0;

 /**
  * Main Loop of the node. It will be executed while the node is active. ros::ok() returns false:
  * - When the node receives the signal SIGINT (Ctrl+C key combination in the terminal where the node is executing).
  * - If another node with the same name starts and substitutes the current node.
  * - When ros::shutdown() is executed elsewhere (for closing the node's communications and finishing it).
  */
  while (ros::ok())
  {
    /**
     * Create an empty message and fill all its fields
     */
    tutorials::positionAngle msg;
    msg.header.seq= iter;
    msg.header.stamp= ros::Time::now();
    msg.angle= angle;
    msg.x= posX;
    msg.y= posY;

    /**
     * Publication of the message through the topic.
     * This method will copy immediately the message to the output buffer of the topic and returns.
     * The message will really be sent later by an internal ROS process when it is possible. 
     */
    pub.publish(msg);

    /**
     * This method processes all waiting callbacks of the node. It will treat all the messages that 
     * are waiting since its last execution. It is not required here since there are no callback
     * functions (associated to topic subscribers or service servers) in this node.
     * Contrary to ros::spin(), this method is not blocking and it will return after treating queued callbacks. 
     * Thereby, we can control the speed for treating the callback queues. In this case, it is important to 
     * well define the size of these queues in order to avoid dropping too many messages.
     */
    // ros::spinOnce();

    /**
     * Show a message through the console and store it in the ROS log system so that it can be read later.
     * Different levels of log messages are possible: ROS_DEBUG, ROS_INFO, ROS_WARN, ROS_ERROR, ROS_FATAL.
     */
    ROS_INFO("Published message %d: %f,%f,%f",msg.header.seq,msg.x,msg.y,msg.angle);
    /**
     * Wait the required time for guaranting the execution frequency defined by loop_rate
     */
    loop_rate.sleep();

    angle= (angle + incrAngle) % 360; 
    iter++;
  }


  return 0;
}
