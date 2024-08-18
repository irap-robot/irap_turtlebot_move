#!/usr/bin/env python3 

import rospy 
from rospkg import RosPack 
import actionlib 
from move_base_msgs.msg import MoveBaseAction ,MoveBaseGoal
from qrdetection.srv import DetectQrcode ,DetectQrcodeResponse

import cv2 
from cv_bridge import CvBridge

import sys 

def movebase_client(position,orientation) : 
    client = actionlib.SimpleActionClient("move_base",MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = position[0]
    goal.target_pose.pose.position.y = position[1]
    goal.target_pose.pose.position.z = position[2]
    goal.target_pose.pose.orientation.x = orientation[0]
    goal.target_pose.pose.orientation.y = orientation[1]
    goal.target_pose.pose.orientation.z = orientation[2]
    goal.target_pose.pose.orientation.w = orientation[3]
    
    client.send_goal(goal)
    wait = client.wait_for_result()

    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()
    
def detect_qrcode_client() : 
    rospy.wait_for_service('detect_qrcode')
    try : 
        detect_qrcode = rospy.ServiceProxy('detect_qrcode',DetectQrcode)
        resp = detect_qrcode()
        return resp.success ,brigde.imgmsg_to_cv2(resp.image) 
    except rospy.ServiceException as e : 
        print("Service call failed: %s"%e)

if __name__ == "__main__" : 
    rospy.init_node("turtlebot_move")
    rp = RosPack()
    dir = rp.get_path("irap_turtlebot_move")

    brigde = CvBridge()

    rate = rospy.Rate(10)
    
    rospy.loginfo("move to point 1")
    movebase_client([-0.55,-0.55,0.0],[0.,0.,-0.356,0.934])
    success ,image = detect_qrcode_client()
    cv2.imwrite(dir+"/image/image1.png", image)
    rospy.sleep(3)

    rospy.loginfo("move to point 2")
    movebase_client([-0.55, 0.46,0.0],[0.,0., 0.898,0.440])
    success ,image = detect_qrcode_client()
    cv2.imwrite(dir+"/image/image2.png", image)
    rospy.sleep(3)

    rospy.loginfo("move to point 3")
    movebase_client([ 0.50, 0.52,0.0],[0.,0., 0.350,0.937])
    success ,image = detect_qrcode_client()
    cv2.imwrite(dir+"/image/image3.png", image)
    rospy.sleep(3)

    rospy.loginfo("move to point 4")
    movebase_client([ 1.14,-0.43,0.0],[0.,0.,-0.707,0.707])
    success ,image = detect_qrcode_client()
    cv2.imwrite(dir+"/image/image4.png", image)
    rospy.sleep(3)