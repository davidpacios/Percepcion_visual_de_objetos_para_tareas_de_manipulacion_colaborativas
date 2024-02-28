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
#include <cstdlib>

int main(int argc, char **argv)
{
  /** 
   * Initialization of a ROS node with name 'add_two_ints_client', 
   * giving acces to line command arguments (argc, argv). The name of the node should be unique.
   */
  ros::init(argc, argv, "add_two_ints_client");
  /**
   * Verification that the user has introduced the required parameters from the command line.
   */
  if (argc != 3)
  {
    ROS_INFO("usage: add_two_ints_client X Y");
    return 1;
  }
   /**
   * Creation of handle for accessing the node. The first handle starts the node
   * (equivalent to ros::start()) and the destruction of the last handle finishes
   * the node (equivalent to ros::shutdown()).
   */
  ros::NodeHandle n;
  /**
   * Creation of the ServiceClient object that will enable the later call of the service.
   * It is the handle for the client connections to the service 'add_two_ints'.
   */
  ros::ServiceClient client = n.serviceClient<tutorials::AddTwoInts>("add_two_ints");
  /**
   * Creation of a service object and completion of its request member.
   */
  tutorials::AddTwoInts srv;
  srv.request.a = atoll(argv[1]);
  srv.request.b = atoll(argv[2]);
  
  /**
   * Call of the service. The client will send the request to the server/provider (request member of srv) and the server
   * will answer with a response. This method is blocking and will only return when the call is done.
   * If the call is correctly executed, it will return true and the response member of srv will be completed.
   * If the call fails, it will return false and the response member of srv will not be correct.
   */
  if (client.call(srv))
  {
    ROS_INFO("Sum: %ld", (long int)srv.response.sum);
  }
  else
  {
    ROS_ERROR("Failed to call service add_two_ints");
    return 1;
  }

  return 0;
}
