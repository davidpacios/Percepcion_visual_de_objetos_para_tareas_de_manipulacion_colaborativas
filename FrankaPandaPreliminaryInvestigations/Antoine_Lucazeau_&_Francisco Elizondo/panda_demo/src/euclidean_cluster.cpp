#include <ros/ros.h>
#include <ros/console.h>
#include <moveit/moveit_cpp/moveit_cpp.h>
// PCL specific includes
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/features/normal_3d.h>
#include <pcl/search/kdtree.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>

#include <pcl/filters/voxel_grid.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/filters/passthrough.h>
#include <pcl/segmentation/extract_clusters.h>
#include <pcl/filters/extract_indices.h>

#include <visualization_msgs/Marker.h>
#include <visualization_msgs/MarkerArray.h>

ros::Publisher pub;
ros::Publisher vis_pub;
ros::Publisher pos_pub;
ros::Publisher euc_pub;

std::vector<float> normal_goal{0.0, 1.0, 0.0};
float epsilon = 0.9;
int sample_size = 5;
std::vector<pcl::PointCloud<pcl::PointXYZI>> cloud_cluster_sampled(sample_size);

visualization_msgs::MarkerArray make_corner_markers (double minx, double maxx, double miny, double maxy, double minz, double maxz) {

  visualization_msgs::MarkerArray marker_array;
  marker_array.markers.resize(8);

  marker_array.markers[0].header.frame_id = "camera_depth_optical_frame";
  marker_array.markers[0].header.stamp = ros::Time();
  marker_array.markers[0].ns = "my_namespace";
  marker_array.markers[0].id = 1;
  marker_array.markers[0].type = visualization_msgs::Marker::SPHERE;
  marker_array.markers[0].action = visualization_msgs::Marker::ADD;
  marker_array.markers[0].pose.position.x = maxx;
  marker_array.markers[0].pose.position.y = maxy;
  marker_array.markers[0].pose.position.z = maxz;
  marker_array.markers[0].pose.orientation.x = 0.0;
  marker_array.markers[0].pose.orientation.y = 0.0;
  marker_array.markers[0].pose.orientation.z = 0.0;
  marker_array.markers[0].pose.orientation.w = 1.0;
  marker_array.markers[0].scale.x = 0.1;
  marker_array.markers[0].scale.y = 0.1;
  marker_array.markers[0].scale.z = 0.1;
  marker_array.markers[0].color.a = 1;
  marker_array.markers[0].color.r = 1.0;
  marker_array.markers[0].color.g = 1.0;
  marker_array.markers[0].color.b = 0.0;

  marker_array.markers[1] = marker_array.markers[0];
  marker_array.markers[2] = marker_array.markers[0];
  marker_array.markers[3] = marker_array.markers[0];
  marker_array.markers[4] = marker_array.markers[0];
  marker_array.markers[5] = marker_array.markers[0];
  marker_array.markers[6] = marker_array.markers[0];
  marker_array.markers[7] = marker_array.markers[0];

  marker_array.markers[4].pose.position.x = minx;
  marker_array.markers[5].pose.position.x = minx;
  marker_array.markers[6].pose.position.x = minx;
  marker_array.markers[7].pose.position.x = minx;

  marker_array.markers[2].pose.position.y = miny;
  marker_array.markers[3].pose.position.y = miny;
  marker_array.markers[6].pose.position.y = miny;
  marker_array.markers[7].pose.position.y = miny;

  marker_array.markers[1].pose.position.z = minz;
  marker_array.markers[3].pose.position.z = minz;
  marker_array.markers[5].pose.position.z = minz;
  marker_array.markers[7].pose.position.z = minz;

  marker_array.markers[1].id = 2;
  marker_array.markers[2].id = 3;
  marker_array.markers[3].id = 4;
  marker_array.markers[4].id = 5;
  marker_array.markers[5].id = 6;
  marker_array.markers[6].id = 7;
  marker_array.markers[7].id = 8;

  return marker_array;
}

class Filter {
  public:
    Filter(double minx, double maxx, double miny, double maxy, double minz, double maxz) {
      
      pass_filter_param.maxx = maxx;
      pass_filter_param.minx = minx;
      pass_filter_param.maxy = maxy;
      pass_filter_param.miny = miny;
      pass_filter_param.maxz = maxz;
      pass_filter_param.minz = minz;

      marker_array = make_corner_markers(minx,maxx,miny,maxy,minz,maxz);

    }

    void cloud_cb (const sensor_msgs::PointCloud2ConstPtr& cloud_msg)
    {
      // Container for original & filtered data
      pcl::PCLPointCloud2::Ptr cloud (new pcl::PCLPointCloud2 ());
      pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_pcl (new pcl::PointCloud<pcl::PointXYZ>);
      pcl::PointCloud<pcl::PointXYZI>::Ptr cloud_pcl_col (new pcl::PointCloud<pcl::PointXYZI>);
      pcl::PointCloud<pcl::PointXYZI>::Ptr cloud_cluster (new pcl::PointCloud<pcl::PointXYZI>);
      pcl::PointCloud<pcl::PointXYZI>::Ptr cloud_cluster_sum (new pcl::PointCloud<pcl::PointXYZI>);

      // Convert to PCL data type
      pcl_conversions::toPCL(*cloud_msg, *cloud);
      pcl::fromPCLPointCloud2 (*cloud, *cloud_pcl);

      pass_through_filter(cloud_pcl);

      if (cloud_pcl->empty()) {
        return;
      }
      voxelize_filter(cloud_pcl);

      if (cloud_pcl->empty()) {
        return;
      }
      copyPointCloud(*cloud_pcl, *cloud_pcl_col);
      euclidean_cluster(cloud_pcl_col, cloud_cluster);

      if (cloud_cluster->empty()) {
        return;
      }

      // For more consistency, use the 4 last point clouds
      cloud_cluster_sampled.pop_back();
      cloud_cluster_sampled.insert(cloud_cluster_sampled.begin(),*cloud_cluster);

      // ROS_INFO_STREAM("Current cloud size : "<<cloud_cluster->size());
      cloud_cluster_sum->header.frame_id = "camera_depth_optical_frame";

      for (int i=0; i < sample_size; i++) {
        // ROS_INFO_STREAM("Sampled cloud n"<<i<<" size : "<<cloud_cluster_sampled[i].size());
        *cloud_cluster_sum += cloud_cluster_sampled[i];

      }

      // ROS_INFO_STREAM("All Sampled cloud size "<<cloud_cluster_sum->size());
      // Publish position
      cluster_position(cloud_cluster_sum);

      // Convert to ROS data type
      pcl::toPCLPointCloud2 (*cloud_cluster_sum, *cloud);


      sensor_msgs::PointCloud2 output;
      pcl_conversions::moveFromPCL(*cloud, output);

      pcl::toPCLPointCloud2 (*cloud_pcl_col, *cloud);

      sensor_msgs::PointCloud2 euclidean;
      pcl_conversions::moveFromPCL(*cloud, euclidean);

      // Publish the data
      pub.publish ( output ) ;
      euc_pub.publish ( euclidean );
      vis_pub.publish( marker_array );
        

      
    }

    void pass_through_filter (const pcl::PointCloud<pcl::PointXYZ>::Ptr& cloud_pcl) {

      pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_pass_ypcl (new pcl::PointCloud<pcl::PointXYZ>);
      pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_pass_xpcl (new pcl::PointCloud<pcl::PointXYZ>);

      pcl::PassThrough<pcl::PointXYZ> pass;
      pass.setInputCloud (cloud_pcl);
      pass.setFilterFieldName ("y");
      pass.setFilterLimits (pass_filter_param.miny, pass_filter_param.maxy);
      pass.filter (*cloud_pass_ypcl);

      pass.setInputCloud (cloud_pass_ypcl);
      pass.setFilterFieldName ("x");
      pass.setFilterLimits (pass_filter_param.minx, pass_filter_param.maxx);
      pass.filter (*cloud_pass_xpcl);

      pass.setInputCloud (cloud_pass_xpcl);
      pass.setFilterFieldName ("z");
      pass.setFilterLimits (pass_filter_param.minz, pass_filter_param.maxz);
      pass.filter (*cloud_pcl);
    }

    void voxelize_filter (const pcl::PointCloud<pcl::PointXYZ>::Ptr& cloud_pcl) {

      pcl::VoxelGrid<pcl::PointXYZ> vg;
      vg.setInputCloud (cloud_pcl);
      vg.setLeafSize (0.01f, 0.01f, 0.01f);
      vg.filter (*cloud_pcl);

    }

    void euclidean_cluster (const pcl::PointCloud<pcl::PointXYZI>::Ptr& cloud_pcl_col, const pcl::PointCloud<pcl::PointXYZI>::Ptr& cloud_cluster) {

      pcl::search::KdTree<pcl::PointXYZI>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZI>);
      tree->setInputCloud (cloud_pcl_col);

      std::vector<pcl::PointIndices> cluster_indices;
      pcl::EuclideanClusterExtraction<pcl::PointXYZI> ec;
      ec.setClusterTolerance (0.02);
      ec.setMinClusterSize (10);
      ec.setMaxClusterSize (25000);
      ec.setSearchMethod (tree);
      ec.setInputCloud (cloud_pcl_col);
      ec.extract (cluster_indices);

      int nbr_cluster = cluster_indices.size ();
      if (nbr_cluster > 0) { 
        int i = 0;
        for (const auto& cluster : cluster_indices) {
          double intensity = (double) i/nbr_cluster;
          for (const auto& idx : cluster.indices) {
            (*cloud_pcl_col)[idx].intensity = intensity;
          }
          i++;
        }

        pcl::PointIndices::Ptr inliers (new pcl::PointIndices ());
        *inliers = cluster_indices[0];
        pcl::ExtractIndices<pcl::PointXYZI> extract;

        extract.setInputCloud (cloud_pcl_col);
        extract.setIndices (inliers);
        extract.setNegative (false);
        extract.filter (*cloud_cluster);
      }
    }

    void cluster_position (const pcl::PointCloud<pcl::PointXYZI>::Ptr& cloud_cluster) {

      int size = cloud_cluster->points.size ();
      double sumx = 0;
      double sumy = 0;
      double sumz = 0;
      double miny = pass_filter_param.maxy;
      for(int nIndex = 0; nIndex < size; nIndex++)
      { 
        double x = cloud_cluster->points[nIndex].x;
        double y = cloud_cluster->points[nIndex].y;
        double z = cloud_cluster->points[nIndex].z;
        sumx += x;
        sumy += y;
        sumz += z;
        if (y < miny) {
          miny = y;
        }
      }
      geometry_msgs::PoseStamped pose_stamped;
      pose_stamped.header.frame_id = "camera_depth_optical_frame";
      pose_stamped.pose.position.x = sumx/size;
      pose_stamped.pose.position.y = miny;
      pose_stamped.pose.position.z = sumz/size;
      pose_stamped.pose.orientation.w = 1.0;
      pos_pub.publish(pose_stamped);

      marker_array.markers.resize(9);
      marker_array.markers[8] = marker_array.markers[0];
      marker_array.markers[8].id = 9;
      marker_array.markers[8].pose = pose_stamped.pose;
      marker_array.markers[8].scale.x = 0.05;
      marker_array.markers[8].scale.y = 0.05;
      marker_array.markers[8].scale.z = 0.05;
      marker_array.markers[8].color.a = 1;
      marker_array.markers[8].color.r = 0.0;
      marker_array.markers[8].color.g = 1.0;
      marker_array.markers[8].color.b = 0.0;


    }

  private:
    struct AddPassFilterParam
    {
      double maxx, minx, maxy, miny, maxz, minz;
    };
    AddPassFilterParam pass_filter_param;
    visualization_msgs::MarkerArray marker_array;
};

int
main (int argc, char** argv)
{
  // Initialize ROS
  ros::init (argc, argv, "euclidean_cluster");
  ros::NodeHandle nh;

  double maxx = -0.3;
  double minx = -0.7;
  double maxy = 0.58;
  double miny = 0.2;
  double maxz = 2.3;
  double minz = 1.8;

  if (argc == 7) {
    minx = atof(argv[1]);
    maxx = atof(argv[2]);
    miny = atof(argv[3]);
    maxy = atof(argv[4]);
    minz = atof(argv[5]);
    maxz = atof(argv[6]);  
  }

  pub = nh.advertise<sensor_msgs::PointCloud2> ("output", 1);
  vis_pub = nh.advertise<visualization_msgs::MarkerArray> ("visualization_marker_array", 0);
  euc_pub = nh.advertise<sensor_msgs::PointCloud2> ("euclidean", 1);
  pos_pub = nh.advertise<geometry_msgs::PoseStamped> ("pick_pose", 0);

  
  Filter filter(minx,maxx,miny,maxy,minz,maxz);
  
  ROS_INFO_STREAM("Starting the euclidean segmentation");
  // Create a ROS subscriber for the input point cloud
  ros::Subscriber sub = nh.subscribe<sensor_msgs::PointCloud2> ("/move_group/kinect/filtered_cloud", 1, &Filter::cloud_cb, &filter);


  // Spin
  ros::spin ();
}
