#!/usr/bin/env python

"""
.. module:: action_user
   :platform: Unix
   :synopsis: A user interface of the project

.. moduleauthor:: Mustafa Melih Toslak

A node that implements an action client, allowing the user to **set a target (x, y) or to cancel** it. The node also **publishes the robot position and velocity** as a custom message (x,y, vel_x, vel_y), by relying on the values published on the topic /odom.

Subscribes to:
    /odom

Publishes to:
    /posxy_velxy
    
Client:
    /reaching_goal

"""


import rospy
import actionlib
import actionlib.msg
import assignment_2_2022.msg
from std_srvs.srv import *
import sys
import select
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Twist
from assignment_2_2022.msg import Posxy_velxy
from colorama import Fore, Style
from colorama import init
init()
 
# callback function for the subscriber
def publisher(msg):
    """
    The *publisher* function in this code is a callback that extracts position 
    and velocity information from a received message and creates a custom message
    *(Posxy_velxy)* with the extracted data. It publishes the custom message on a
    topic for further use by other nodes in the system.
    
    """
    global pub
    # get the position information
    pos = msg.pose.pose.position
    # get the velocity information
    velocity = msg.twist.twist.linear
    # custom message
    posxy_velxy = Posxy_velxy()
    # assign the parameters of the custom message
    posxy_velxy.msg_pos_x = pos.x
    posxy_velxy.msg_pos_y = pos.y
    posxy_velxy.msg_vel_x = velocity.x
    posxy_velxy.msg_vel_y = velocity.y
    # publish the custom message
    pub.publish(posxy_velxy)

def action_client():
    """
    The action_client function creates an action client that interacts with an action 
    server to send goals for reaching a target position. It prompts the user to enter 
    the target position and sends the goal to the server. It also provides the option 
    to cancel the goal if 'c' is entered.
    
    """
    # create the action client
    action_client = actionlib.SimpleActionClient('/reaching_goal', assignment_2_2022.msg.PlanningAction)
    # wait for the server to be started
    action_client.wait_for_server()
    
    status_goal = False
	
    while not rospy.is_shutdown():
        # Get the keyboard inputs
        print(Fore.GREEN + "Please enter position of the target or type c to cancel it ")
        #print(Fore.MAGENTA + "X position of target: ")
        x_pos_input = input(Fore.MAGENTA + "X position of target: ")
        #print(Fore.MAGENTA + "Y position of target: ")
        y_pos_input = input(Fore.MAGENTA + "Y position of target: ")
        
 	# If user entered 'c' cancel the goal
        if x_pos_input == "c" or y_pos_input == "c":
            # Cancel the goal
            action_client.cancel_goal()
            status_goal = False
        else:
            # Convert numbers from string to float
            x_pos_send = float(x_pos_input)
            y_pos_send = float(y_pos_input)
            # Create the goal to send to the server
            goal = assignment_2_2022.msg.PlanningGoal()
            goal.target_pose.pose.position.x = x_pos_send
            goal.target_pose.pose.position.y = y_pos_send
					
            # Send the goal to the action server
            action_client.send_goal(goal)
            status_goal = True


def main():
    # initialize the node
    rospy.init_node('action_user')
    # global publisher
    global pub
    # publisher: send a message which contains two parameters (velocity and position)
    pub = rospy.Publisher("/posxy_velxy", Posxy_velxy, queue_size = 1)
    # subscriber: get from "Odom" two parameters (velocity and position)
    sub_from_Odom = rospy.Subscriber("/odom", Odometry, publisher)
    # call the function action_client
    action_client()

if __name__ == '__main__':
    main()

