#!/usr/bin/env python

from __future__ import print_function
from six.moves import input

import rospy
import sys

import tf_conversions

import tf
import tf2_ros
import geometry_msgs.msg

from math import pi, tau

def broadcast_user_pose(x,y,z,tx,ty,tz):
    br = tf2_ros.StaticTransformBroadcaster()
    t = geometry_msgs.msg.TransformStamped()

    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "world"
    t.child_frame_id = "camera_link"
    t.transform.translation.x = x
    t.transform.translation.y = y
    t.transform.translation.z = z
    q = tf_conversions.transformations.quaternion_from_euler(tx, ty, tz)
    t.transform.rotation.x = q[0]
    t.transform.rotation.y = q[1]
    t.transform.rotation.z = q[2]
    t.transform.rotation.w = q[3]

    print(x,y,z,q[0],q[1],q[2],q[3])

    br.sendTransform(t)

def main():
    rospy.init_node('camera_position_calibrator')
    myargv = rospy.myargv(argv=sys.argv)
    # x = float(input("x : "))
    # y = float(input("y : "))
    # z = float(input("z : "))
    # tx = float(input("tx : "))/360*tau
    # ty = float(input("ty : "))/360*tau
    # tz = float(input("tz : "))/360*tau
    x = float(myargv[1])
    y = float(myargv[2])
    z = float(myargv[3])
    tx = float(myargv[4])/360*tau
    ty = float(myargv[5])/360*tau
    tz = float(myargv[6])/360*tau
    broadcast_user_pose(x,y,z,tx,ty,tz)
    rospy.sleep(0.5)

if __name__ == "__main__":
    main()
