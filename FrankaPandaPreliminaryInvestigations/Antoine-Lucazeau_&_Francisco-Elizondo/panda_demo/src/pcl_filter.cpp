#include <ros/ros.h>
#include <ros/console.h>
// PCL specific includes
#include <sensor_msgs/PointCloud2.h>
#include <pcl/ModelCoefficients.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>

#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/filters/extract_indices.h>

ros::Publisher pub;

std::vector<float> normal_goal{0.0, 1.0, 0.0};
float epsilon = 0.9;

void 
cloud_cb (const sensor_msgs::PointCloud2ConstPtr& cloud_msg)
{

  // Container for original & filtered data
  pcl::PCLPointCloud2::Ptr cloud (new pcl::PCLPointCloud2 ());
  pcl::PCLPointCloud2::Ptr cloud_filtered (new pcl::PCLPointCloud2 ());
  pcl::PCLPointCloud2::Ptr plane_cloud (new pcl::PCLPointCloud2 ());

  pcl::PointCloud<pcl::PointXYZ>::Ptr pcl_cloud_filtered (new pcl::PointCloud<pcl::PointXYZ>);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_p (new pcl::PointCloud<pcl::PointXYZ>);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_f (new pcl::PointCloud<pcl::PointXYZ>);

  // Convert to PCL data type
  pcl_conversions::toPCL(*cloud_msg, *cloud);

  // Perform the actual filtering
  pcl::VoxelGrid<pcl::PCLPointCloud2> sor;
  sor.setInputCloud (cloud);
  sor.setLeafSize (0.1, 0.1, 0.1);
  sor.filter (*cloud_filtered);

  // Convert to PCL data type
  pcl::fromPCLPointCloud2 (*cloud_filtered, *pcl_cloud_filtered);

  pcl::ModelCoefficients::Ptr coefficients (new pcl::ModelCoefficients ());


  pcl::PointIndices::Ptr inliers (new pcl::PointIndices ());
  // Create the segmentation object
  pcl::SACSegmentation<pcl::PointXYZ> seg;
  // Optional
  seg.setOptimizeCoefficients (true);
  // Mandatory
  seg.setModelType (pcl::SACMODEL_PLANE);
  seg.setMethodType (pcl::SAC_RANSAC);
  seg.setMaxIterations (1000);
  seg.setDistanceThreshold (0.01);

  // Create the filtering object
  pcl::ExtractIndices<pcl::PointXYZ> extract;

  //Loop until we have found the biggest plane of the right normal
  int nr_points = (int) pcl_cloud_filtered->size ();
  bool found_table = false;
  float scalar_prod = 0;
  while (scalar_prod < epsilon) {
    //use segmentation to find the plane
    seg.setInputCloud (pcl_cloud_filtered);
    seg.segment (*inliers, *coefficients);

    //if no plane has been found stop the loop
    if ((inliers->indices.size () == 0) || (pcl_cloud_filtered->size () < 0.1 * nr_points)) {
      ROS_INFO_STREAM("Could not find the table");
      break;
    }

    //filter the plane out
    extract.setInputCloud (pcl_cloud_filtered);
    extract.setIndices (inliers);
    extract.setNegative (false);
    extract.filter (*cloud_p);

    //remove the plane from the remaining cloud
    extract.setNegative (true);
    extract.filter (*cloud_f);
    pcl_cloud_filtered.swap (cloud_f);

    //check if we have identified the table
    std::vector<float> coeff_vec = coefficients->values;
    std::vector<float> normal(coeff_vec.begin(), coeff_vec.begin()+3);
 
    scalar_prod = abs(std::inner_product(std::begin(normal_goal), std::end(normal_goal), std::begin(normal), 0.0));
    

  }

  ROS_INFO_STREAM(coefficients->values[3]);
  pcl::toPCLPointCloud2 (*cloud_p, *plane_cloud);

  // Convert to ROS data type
  sensor_msgs::PointCloud2 output;
  pcl_conversions::moveFromPCL(*plane_cloud, output);

  // Publish the data
  pub.publish (output);
}

int
main (int argc, char** argv)
{
  // Initialize ROS
  ros::init (argc, argv, "my_pcl_tutorial");
  ros::NodeHandle nh;

  // Create a ROS subscriber for the input point cloud
  ros::Subscriber sub = nh.subscribe<sensor_msgs::PointCloud2> ("/camera/depth/points", 1, cloud_cb);

  // Create a ROS publisher for the output point cloud
  pub = nh.advertise<sensor_msgs::PointCloud2> ("output", 1);

  // Spin
  ros::spin ();
}
