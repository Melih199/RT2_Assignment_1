#! /usr/bin/env python

"""
.. module:: print_dis_avgvel
   :platform: Unix
   :synopsis: A node provides a Information screen

.. moduleauthor:: Mustafa Melih Toslak

The third node prints out information about a robot's distace from target and average velocity. The node gets the publish frequency parameter from ROS parameters, which is used to determine how often the information is printed. It also initializes a variable to keep track of the last time the information was printed and creates a subscriber to the '/posxy_velxy' topic, which i to containining messages of robot's curren x,y positions and x,y velocities.

Subscribes to:
    /posxy_velxy

"""

import rospy
import math
import time
from assignment_2_2022.msg import Posxy_velxy
from colorama import init
init()
from colorama import Fore, Back, Style

class PrintInfo:
    def __init__(self):
        # Get the publish frequency parameter
        self.freq = rospy.get_param("frequency")

        # Last time the info was printed
        self.printed = 0

        # Subscriber to the position and velocity topic
        self.sub_pos = rospy.Subscriber("/posxy_velxy", Posxy_velxy, self.posvel_callback)

    def posvel_callback(self, msg):
        # Compute time period in milliseconds
        period = (1.0/self.freq) * 1000
        
        # Get current time in milliseconds
        curr_time = time.time() * 1000

        # Check if the current time minus the last printed time is greater than the period
        if curr_time - self.printed > period:
            # Get the desired position from ROS parameters
            target_x = rospy.get_param("des_pos_x")
            target_y = rospy.get_param("des_pos_y")

            # Get the actual position of the robot from the message
            robot_x = msg.msg_pos_x
            robot_y = msg.msg_pos_y

            # Compute the distance between the desired and actual positions
            distance = round(math.dist([target_x, target_y], [robot_x, robot_y]),2)
            
            # Get the actual velocity of the robot from the message
            vel_x = msg.msg_vel_x
            vel_y = msg.msg_vel_y           

            # Compute the average speed using the velocity components from the message
            average_speed = round(math.sqrt(vel_x**2 + vel_y**2),2)

            # Print the distance and speed information
            rospy.loginfo(Fore.GREEN + "Distance to target: %s [m]", distance)
            rospy.loginfo(Fore.MAGENTA + "Robot average speed: %s [m/s]", average_speed)

            # Update the last printed time
            self.printed = curr_time

def main():
	
    # Suppress the timestamps from the log messages
    #rospy.set_param('/rosconsole/formatter/time', 'none') I tried to delete time values from scren but it didn`t work	
    
    # Initialize the node
    rospy.init_node('print_dis_avgvel')
    
    # Create an instance of the PrintInfo class
    print_dis_avgvel = PrintInfo()
    
    # Wait for messages
    rospy.spin()

if __name__ == "__main__":
    main()

