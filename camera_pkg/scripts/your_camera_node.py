#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from sensor_msgs.msg import CameraInfo

k1 = -0.042486062
k2 = 0.81350574
t1 = -0.0048942071
t2 = 0.0018472401
k3 = -3.2331309
fx = 653.1650038
cx = 317.900734
fy = 653.5617567
cy = 260.1273618

camera_info = CameraInfo()
camera_info.width = 640
camera_info.height = 480
camera_info.distortion_model = "plumb_bob"
camera_info.D = [k1, k2, t1, t2, k3]
camera_info.K = [fx, 0, cx, 0, fy, cy, 0, 0, 1]
camera_info.R = [1, 0, 0, 0, 1, 0, 0, 0, 1]
camera_info.P = [fx, 0, cx, 0, 0, fy, cy, 0, 0, 0, 1, 0]

def main():
    # Initialize the node
    rospy.init_node('your_camera_node')
    print(" Started Cam Node")

    # Create a publisher for the camera frames
    pub = rospy.Publisher('/image_rect', Image, queue_size=10)
    pub2 = rospy.Publisher('/camera_info', CameraInfo, queue_size=10)

    # Create a CvBridge object
    bridge = CvBridge()

    # Open the camera
    cap = cv2.VideoCapture(0)

    # Set the camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Loop until the node is shutdown
    while not rospy.is_shutdown():
        # Capture a frame from the camera
        ret, frame = cap.read()

        # Convert the frame to a ROS message
        if ret:
            msg = bridge.cv2_to_imgmsg(frame, encoding='bgr8')

            # Publish the message
            pub.publish(msg)
            pub2.publish(camera_info)


    # Release the camera
    cap.release()

if __name__ == '__main__':
    main()