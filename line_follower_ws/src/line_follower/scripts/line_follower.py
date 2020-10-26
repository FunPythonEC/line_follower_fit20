#!/usr/bin/env python
from sensor_msgs.msg import Image
from std_msgs.msg import Int16
import rospy, cv2, cv_bridge, numpy


class line_follower(object):
    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")
        h, w, d = cv_image.shape

        lower = numpy.array([10, 15, 70], dtype="uint8")
        upper = numpy.array([100, 140, 220], dtype="uint8")
        mask = cv2.inRange(cv_image, lower, upper)

        output = cv2.bitwise_and(cv_image, cv_image, mask=mask)
        output[
            numpy.where(
                (output[:, :, 0] > 82)
                & (output[:, :, 0] < 95)
                & (output[:, :, 1] > 97)
                & (output[:, :, 1] < 108)
                & (output[:, :, 2] > 83)
                & (output[:, :, 2] < 97)
            )
        ] = [0, 0, 0]
        output[
            numpy.where(
                (output[:, :, 0] > 10)
                & (output[:, :, 0] < 78)
                & (output[:, :, 1] > 30)
                & (output[:, :, 1] < 125)
                & (output[:, :, 2] > 60)
                & (output[:, :, 2] < 190)
            )
        ] = [255, 255, 255]

        gray_image = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
        ret, thresh = cv2.threshold(gray_image, 127, 255, 0)

        M = cv2.moments(thresh)
        masked_image_msg = self.bridge.cv2_to_imgmsg(output, "rgb8")
        cX = int(M["m10"] / M["m00"])
        err = cX -20 - w / 2
	print("Error position: ", err)

        # 	cv2.imshow("mask",output)
        self.processed_image_pub.publish(masked_image_msg)
        self.motors_pwr.data = err
        self.motors_pwr_pub.publish(self.motors_pwr)

    def __init__(self):

        rospy.init_node("line_follower_processor", anonymous=True)
        rospy.Subscriber("/usb_cam/image_raw", Image, self.image_callback)

        self.bridge = cv_bridge.CvBridge()

        # variables
        self.motors_pwr = Int16()
        self.motors_pwr_pub = rospy.Publisher("/motors_pwr", Int16, queue_size=1)
        self.processed_image_pub = rospy.Publisher(
            "/line_follower/processed_image", Image, queue_size=1
        )
        self.processed_image = Image()
        self.processed_image.width = 640
        self.processed_image.height = 480
        # self.boundaries = [([5, 5, 50], [25, 25, 145])]


def image_listener():
    rospy.init_node("line_follower_processor", anonymous=True)
    rospy.Subscriber("/usb_cam/image_raw", Image, image_callback)
    rospy.spin()


if __name__ == "__main__":
    robot = line_follower()
    while not rospy.is_shutdown():
        pass
