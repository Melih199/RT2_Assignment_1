#! /usr/bin/env python

"""
.. module:: goal_service
   :platform: Unix
   :synopsis: A sevice node for counting targets

.. moduleauthor:: Mustafa Melih Toslak

This node provides a service (goal_service) to track the number of goals reached and cancelled. It initializes counters for goals reached and cancelled. It also subscribes to the /reaching_goal/result topic to receive status updates of goal results.

Subscribes to:
    /reaching_goal/result


"""
import rospy # Import the ROS python library
from assignment_2_2022.srv import goal_rc, goal_rcResponse # Import the service and service response messages
import actionlib   # Import the actionlib library
import actionlib.msg  # Import the actionlib message library
import assignment_2_2022.msg  # Import the package message library




class Service:
    """
    The Service class represents a ROS service for tracking the number of goals reached and cancelled. 
    
    """
    def __init__(self):
        # Initialize the counters for goals reached and cancelled
        self.goal_cancelled = 0
        self.goal_reached   = 0

        # Create the service
        self.srv = rospy.Service('goal_service', goal_rc, self.data)

        # Subscribe to the result topic
        self.sub_result = rospy.Subscriber('/reaching_goal/result', assignment_2_2022.msg.PlanningActionResult, self.result_callback)

    def result_callback(self, msg):
        """
        The result_callback function receives a message and extracts the status value. If the status 
        is 2, it increments the goal_cancelled counter. If the status is 3, it increments the 
        goal_reached counter.
    
        """
        # Get the status of the result from the msg
        status = msg.status.status

        # Goal cancelled (status = 2)
        if status == 2:
            self.goal_cancelled += 1

        # Goal reached (status = 3)
        elif status == 3:
            self.goal_reached += 1
    
    def data(self, req):
        """
        The data method is a callback function for the goal_service service.  It creates and returns 
        a response (goal_rcResponse) containing the current values of goal_cancelled and 
        goal_reached counters.
    
        """
        # Return the response containing the current values of goal_cancelled and goal_reached
        return goal_rcResponse(self.goal_reached, self.goal_cancelled)

def main():

    # Initialize the node
    rospy.init_node('goal_service')
    
    # Create an instance of the Service class
    goal_service = Service()
    
    # Wait for messages
    rospy.spin()

if __name__ == "__main__":
    main()

